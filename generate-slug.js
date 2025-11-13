#!/usr/bin/env node
/**
 * Generate slug.json from products folder HTML files
 * This script scans all HTML files in the products folder and creates a mapping
 * of product slugs to their IDs for easy navigation
 */

const fs = require('fs');
const path = require('path');

const PRODUCTS_DIR = path.join(__dirname, 'products');
const OUTPUT_FILE = path.join(__dirname, 'slug.json');

function extractIdFromFilename(filename) {
    // Extract ID from filename like "product-name-123.html"
    const match = filename.match(/-(\d+)\.html$/);
    return match ? match[1] : null;
}

function createSlugFromFilename(filename) {
    // Remove the .html extension and return the full slug
    return filename.replace('.html', '');
}

function generateSlugMapping() {
    try {
        // Check if products directory exists
        if (!fs.existsSync(PRODUCTS_DIR)) {
            console.error('❌ Products directory not found!');
            process.exit(1);
        }

        // Read all files in products directory
        const files = fs.readdirSync(PRODUCTS_DIR);
        const htmlFiles = files.filter(file => file.endsWith('.html'));

        console.log(`📂 Found ${htmlFiles.length} HTML files in products folder`);

        // Create slug mapping
        const slugMapping = {};

        htmlFiles.forEach(filename => {
            const slug = createSlugFromFilename(filename);
            const id = extractIdFromFilename(filename);

            if (id) {
                slugMapping[slug] = {
                    id: parseInt(id),
                    filename: filename,
                    slug: slug
                };
            }
        });

        // Save to slug.json
        fs.writeFileSync(
            OUTPUT_FILE,
            JSON.stringify(slugMapping, null, 2),
            'utf8'
        );

        console.log(`✅ Successfully generated slug.json with ${Object.keys(slugMapping).length} entries`);
        console.log(`📝 File saved to: ${OUTPUT_FILE}`);

        return slugMapping;

    } catch (error) {
        console.error('❌ Error generating slug mapping:', error);
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    generateSlugMapping();
}

module.exports = { generateSlugMapping };
