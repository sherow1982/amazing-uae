const fs = require('fs');
const path = require('path');

const productsDir = './products';
const outputFile = './products-data.json';

const products = [];

const files = fs.readdirSync(productsDir).filter(f => f.endsWith('.html'));

console.log(`Found ${files.length} HTML files`);

files.forEach((file, index) => {
    try {
        const content = fs.readFileSync(path.join(productsDir, file), 'utf-8');
        
        const titleMatch = content.match(/<h1[^>]*class="product-title"[^>]*>([^<]+)<\/h1>/);
        const priceMatch = content.match(/<span class="currency">[^<]+<\/span>([\d.]+)/);
        const imageMatch = content.match(/<meta property="og:image" content="([^"]+)"/);
        const linkMatch = content.match(/href="(https:\/\/www\.amazon\.ae\/dp\/[^"]+)"/);
        const idMatch = content.match(/كود المنتج: (\d+)/);
        
        if (titleMatch && priceMatch && imageMatch && linkMatch && idMatch) {
            products.push({
                id: parseInt(idMatch[1]),
                title: titleMatch[1].trim(),
                price: parseFloat(priceMatch[1]),
                image_link: imageMatch[1],
                affiliate_link: linkMatch[1],
                slug: file.replace('.html', '')
            });
        } else {
            console.log(`Skipping ${file} - missing data`);
        }
    } catch (error) {
        console.error(`Error processing ${file}:`, error.message);
    }
});

fs.writeFileSync(outputFile, JSON.stringify(products, null, 2));
console.log(`\n✓ Generated ${products.length} products in ${outputFile}`);
