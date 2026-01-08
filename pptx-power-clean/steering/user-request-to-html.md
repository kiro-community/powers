---
inclusion: manual
---

# User Request to HTML Preview Guide

This guide covers the complete workflow from user request to HTML preview, before generating the final PowerPoint.

## Overview

**CRITICAL**: Always create an HTML preview first for user review before generating individual slide files and PPTX.

**Workflow:**
1. Understand user requirements
2. Design presentation structure
3. Create single-page HTML preview
4. Get user approval
5. Then proceed to individual slides and PPTX generation

## Step 1: Understand Requirements

**Ask clarifying questions:**
- What is the presentation about?
- Who is the target audience?
- How many slides are needed?
- Any specific branding or color preferences?
- Any charts, images, or special content?

**Analyze the content:**
- Main message or theme
- Key points to communicate
- Logical flow and structure
- Visual style that matches the topic

## Step 2: Design Presentation Structure

**Create an outline:**
```
Slide 1: Title/Cover
- Main title
- Subtitle or tagline
- Optional: Author/date

Slide 2: Introduction/Overview
- Context or background
- What this presentation covers

Slide 3-N: Main Content
- One key point per slide
- Supporting details
- Visual elements if needed

Final Slide: Conclusion/Summary
- Key takeaways
- Call to action or next steps
```

**Choose design elements:**
- Color palette (3-5 colors that match the topic)
- Typography (web-safe fonts only)
- Layout style (minimal, bold, professional, creative)
- Visual hierarchy

## Step 3: Create HTML Preview

**CRITICAL**: Create a single-page HTML file with all slides for easy review.

**CRITICAL: File Organization**

All presentation files MUST be organized in a dedicated folder:

```
[presentation-name]/
├── preview.html                    # For user review
├── slide1.html                     # Created after approval
├── slide2.html
├── ...
├── [presentation-name].pptx        # Final output
└── [presentation-name]-thumbnails.jpg  # Validation
```

**Example:**
```
ai-agents-presentation/
├── preview.html
├── slide1.html (created after approval)
├── slide2.html
├── ...
├── ai-agents-presentation.pptx
└── ai-agents-presentation-thumbnails.jpg
```

**File naming rules:**
- Folder name: Use kebab-case (lowercase with hyphens)
- Preview: `preview.html`
- Slide files: `slide1.html`, `slide2.html`, etc.
- Output PPTX: `[presentation-name].pptx` (matches folder name)
- Thumbnails: `[presentation-name]-thumbnails.jpg`

### Preview HTML Template

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>[Presentation Title] - Preview</title>
  <style>
    body {
      margin: 0;
      padding: 20px;
      background: #1a1a1a;
      font-family: Arial, sans-serif;
    }
    
    .slide {
      width: 960px;
      height: 540px;
      margin: 20px auto;
      background: #0A0E27;  /* Adjust to your color scheme */
      color: #FAFAFA;
      padding: 40px 60px;
      box-sizing: border-box;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
      page-break-after: always;
      position: relative;
    }
    
    .slide h1 {
      font-size: 36pt;
      font-weight: 900;
      margin: 0 0 20px 0;
      color: #00D9FF;  /* Adjust to your accent color */
      line-height: 1.2;
    }
    
    .slide h2 {
      font-size: 28pt;
      font-weight: 700;
      margin: 0 0 15px 0;
      color: #00D9FF;
    }
    
    .slide p {
      font-size: 18pt;
      line-height: 1.5;
      margin: 0 0 15px 0;
      color: #F1F5F9;
    }
    
    .slide ul {
      font-size: 18pt;
      line-height: 1.6;
      margin: 0;
      padding-left: 30px;
    }
    
    .slide li {
      margin-bottom: 10px;
    }
    
    .slide-number {
      position: absolute;
      bottom: 20px;
      right: 30px;
      font-size: 14pt;
      opacity: 0.5;
    }
    
    .source {
      position: absolute;
      bottom: 20px;
      left: 30px;
      font-size: 12pt;
      opacity: 0.7;
    }
    
    /* Title slide specific */
    .slide.title {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
    
    .slide.title h1 {
      font-size: 48pt;
      margin-bottom: 20px;
    }
    
    .slide.title p {
      font-size: 24pt;
      opacity: 0.9;
    }
  </style>
</head>
<body>

  <!-- Slide 1: Title -->
  <div class="slide title">
    <h1>Your Presentation Title</h1>
    <p>Subtitle or tagline</p>
    <div class="slide-number">1</div>
  </div>

  <!-- Slide 2: Content -->
  <div class="slide">
    <h1>Slide Title</h1>
    <p>Main content goes here...</p>
    <ul>
      <li>Key point 1</li>
      <li>Key point 2</li>
      <li>Key point 3</li>
    </ul>
    <div class="slide-number">2</div>
  </div>

  <!-- Add more slides as needed -->

</body>
</html>
```

### Preview Dimensions

**Use larger dimensions for readability:**
- Width: 960px (1.33× the final 720pt)
- Height: 540px (1.33× the final 405pt)
- Maintains 16:9 aspect ratio
- Easier to read and review

**Font sizes for preview:**
- Title (h1): 36-48pt
- Subtitle (h2): 24-32pt
- Body text (p): 18-20pt
- Small text: 14-16pt

## Step 4: Present Preview to User

**Save the file in a dedicated folder:**

Create a folder for the presentation and save the preview:
```bash
mkdir [presentation-name]
# Save preview.html inside this folder
```

**Examples:**
- `ai-agents-presentation/preview.html`
- `quarterly-results/preview.html`
- `product-launch/preview.html`

**Ask for feedback:**
```
"I've created a preview HTML file: [folder-name]/preview.html

Please open it in your browser to review:
- Content and messaging
- Visual design and colors
- Slide flow and structure
- Any missing information

Let me know if you'd like any changes before I generate the PowerPoint."
```

## Step 5: Iterate Based on Feedback

**Common feedback types:**

1. **Content changes:**
   - Add/remove slides
   - Modify text
   - Reorder slides
   - Add more details

2. **Design changes:**
   - Different colors
   - Font adjustments
   - Layout modifications
   - Visual hierarchy

3. **Structure changes:**
   - Different flow
   - Combine/split slides
   - Add sections

**Update the preview HTML** and ask for review again until approved.

## Step 6: Proceed to PPTX Generation

**Only after user approval**, proceed to:
1. Create individual slide HTML files in the same folder (720pt × 405pt)
2. Adjust font sizes for smaller dimensions
3. Use html2pptx tool to generate PPTX in the same folder
4. Generate thumbnails for final validation

**Final folder structure:**
```
[presentation-name]/
├── preview.html
├── slide1.html
├── slide2.html
├── slide3.html
├── ...
└── [presentation-name].pptx
```

See `html2pptx-guide.md` for detailed instructions.

## Design Guidelines for Preview

### Color Palette Selection

**Match colors to content:**
- **Tech/AI**: Blues, cyans, purples (#00D9FF, #667EEA, #764BA2)
- **Business**: Navy, gray, gold (#1C2833, #5D6D7E, #F39C12)
- **Creative**: Bold colors, high contrast (#E74C3C, #F1C40F, #9B59B6)
- **Healthcare**: Greens, blues, white (#27AE60, #3498DB, #ECF0F1)
- **Finance**: Dark blue, green, gray (#154360, #229954, #566573)

**Ensure contrast:**
- Text must be clearly readable on backgrounds
- Use light text on dark backgrounds or vice versa
- Test readability at actual size

### Typography

**Web-safe fonts only:**
- Arial (clean, modern)
- Helvetica (professional)
- Georgia (elegant, readable)
- Verdana (clear, web-friendly)
- Tahoma (compact, clean)
- Trebuchet MS (modern, friendly)

**Font hierarchy:**
```
Title: 36-48pt, bold
Subtitle: 24-32pt, semi-bold
Body: 18-20pt, regular
Small text: 14-16pt, regular
```

### Layout Patterns

**Title slide:**
- Centered content
- Large title
- Subtitle or tagline
- Minimal decoration

**Content slide:**
- Clear heading
- 3-5 bullet points OR
- 2-3 paragraphs OR
- Combination of text and visual placeholder

**Section divider:**
- Large section title
- Optional subtitle
- Minimal content

**Conclusion:**
- Summary points
- Call to action
- Contact info or next steps

## Common Mistakes to Avoid

**DON'T:**
- ❌ Skip the preview step
- ❌ Use final slide dimensions (too small to read)
- ❌ Create individual slides before user approval
- ❌ Use non-web-safe fonts
- ❌ Overcrowd slides with too much text
- ❌ Use poor color contrast
- ❌ Forget slide numbers

**DO:**
- ✅ Create preview first
- ✅ Use readable dimensions (960px × 540px)
- ✅ Get user approval before proceeding
- ✅ Use web-safe fonts
- ✅ Keep slides focused (one idea per slide)
- ✅ Ensure good contrast
- ✅ Number all slides

## Example: Complete Workflow

**User request:**
"Create a presentation about AI agents in different industries"

**Step 1: Clarify**
- How many slides? → 8 slides
- Target audience? → Business executives
- Tone? → Professional but engaging
- Colors? → Tech-focused, modern

**Step 2: Structure**
```
1. Title: "AI Agents Across Industries"
2. Overview: What are AI agents?
3. Healthcare applications
4. Finance applications
5. Retail applications
6. Manufacturing applications
7. Key benefits
8. Conclusion
```

**Step 3: Create preview**
- Create folder: `ai-agents-presentation/`
- Save as `ai-agents-presentation/preview.html`
- Use blue/cyan color scheme
- Professional layout
- Clear hierarchy

**Step 4: Get approval**
"Please review ai-agents-presentation/preview.html. Let me know if you'd like any changes."

**Step 5: User feedback**
"Looks good! Can you add a slide about education?"

**Step 6: Update preview**
- Add slide 6: Education applications
- Renumber remaining slides
- Get final approval

**Step 7: Generate PPTX**
- Create individual slide files in `ai-agents-presentation/`
- Adjust dimensions and fonts
- Use html2pptx tool
- Output: `ai-agents-presentation/ai-agents-presentation.pptx`
- Generate thumbnails

## Tips for Success

1. **Start with content, then design**
   - Get the message right first
   - Then make it look good

2. **Less is more**
   - One key point per slide
   - Use visuals to support, not decorate
   - White space is your friend

3. **Consistency matters**
   - Same fonts throughout
   - Consistent colors
   - Predictable layout patterns

4. **Test readability**
   - Can you read it from 6 feet away?
   - Is the contrast sufficient?
   - Are fonts large enough?

5. **Get feedback early**
   - Preview catches issues before PPTX generation
   - Easier to iterate on HTML than PPTX
   - Saves time and effort

## Next Steps

After user approves the preview:
1. Read `html2pptx-guide.md` for conversion instructions
2. Create individual slide HTML files
3. Use html2pptx MCP tool
4. Generate thumbnails for validation

---

**Remember:** The preview step is crucial for success. It ensures alignment with user expectations before investing time in PPTX generation.
