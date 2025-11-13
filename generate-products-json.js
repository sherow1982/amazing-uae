const fs = require('fs');
const path = require('path');

const productsDir = './products';
const outputFile = './products-data.json';

const products = [];

const files = fs.readdirSync(productsDir).filter(f => f.endsWith('.html'));

files.forEach((file, index) => {
    const content = fs.readFileSync(path.join(productsDir, file), 'utf-8');
    
    const titleMatch = content.match(/<h1[^>]*>([^<]+)<\/h1>/);
    const priceMatch = content.match(/class="price"[^>]*>([\d.]+)/);
    const imageMatch = content.match(/<meta property="og:image" content="([^"]+)"/);
    const linkMatch = content.match(/<a[^>]*href="(https:\/\/www\.amazon\.ae[^"]+)"/);
    
    if (titleMatch && priceMatch && imageMatch && linkMatch) {
        products.push({
            id: index + 1,
            title: titleMatch[1].trim(),
            price: parseFloat(priceMatch[1]),
            image_link: imageMatch[1],
            affiliate_link: linkMatch[1],
            slug: file.replace('.html', '')
        });
    }
});

fs.writeFileSync(outputFile, JSON.stringify(products, null, 2));
console.log(`Generated ${products.length} products in ${outputFile}`);
