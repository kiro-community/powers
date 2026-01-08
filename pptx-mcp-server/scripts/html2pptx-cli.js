#!/usr/bin/env node
/**
 * CLI wrapper for html2pptx library
 * 
 * Usage: node html2pptx-cli.js config.json
 * 
 * Config format:
 * {
 *   "html_files": ["slide1.html", "slide2.html"],
 *   "output_file": "output.pptx",
 *   "config": {}
 * }
 */

const fs = require('fs');
const path = require('path');

// Save original working directory BEFORE changing it
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
    // Read configuration
    const configData = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const { html_files, output_file, config = {} } = configData;

    if (!html_files || !Array.isArray(html_files) || html_files.length === 0) {
      throw new Error('html_files must be a non-empty array');
    }

    if (!output_file) {
      throw new Error('output_file is required');
    }

    // Convert relative paths to absolute based on original working directory
    const absoluteHtmlFiles = html_files.map(f => 
      path.isAbsolute(f) ? f : path.join(originalCwd, f)
    );
    const absoluteOutputFile = path.isAbsolute(output_file) ? 
      output_file : path.join(originalCwd, output_file);

    // Create presentation
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';  // Default to 16:9

    console.log(`Converting ${html_files.length} HTML slides to PowerPoint...`);

    // Process each HTML file
    for (let i = 0; i < absoluteHtmlFiles.length; i++) {
      const htmlFile = absoluteHtmlFiles[i];
      console.log(`  Processing slide ${i + 1}/${html_files.length}: ${path.basename(htmlFile)}`);
      
      try {
        const { slide, placeholders } = await html2pptx(htmlFile, pptx);
        
        if (placeholders && placeholders.length > 0) {
          console.log(`    Found ${placeholders.length} placeholder(s)`);
        }
      } catch (error) {
        console.error(`    Error processing ${htmlFile}: ${error.message}`);
        throw error;
      }
    }

    // Save presentation
    console.log(`Saving presentation to: ${path.basename(absoluteOutputFile)}`);
    await pptx.writeFile({ fileName: absoluteOutputFile });
    
    console.log(`✓ Successfully created ${absoluteOutputFile}`);
    console.log(`  Total slides: ${html_files.length}`);

  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
