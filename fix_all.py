import os
import re
import json

# مسار المجلد
repo_path = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
products_dir = os.path.join(repo_path, 'products')

print("=== Starting Fix ===\n")

# 1. إصلاح روابط style.css
print("1. Fixing style.css links...")
html_files = []
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

pattern = r'<link\s+rel="stylesheet"\s+href="[^"]*style\.css[^"]*">'
modified_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, r'<!-- \g<0> -->', content)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_count += 1
            print(f"   ✓ {os.path.basename(html_file)}")
    except Exception as e:
        print(f"   ✗ Error: {html_file}")

print(f"   Done! Modified {modified_count} files\n")

# 2. توليد products-data.json
print("2. Generating products-data.json...")
products = []
product_files = [f for f in os.listdir(products_dir) if f.endswith('.html')]

for idx, file in enumerate(product_files):
    try:
        filepath = os.path.join(products_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'<h1[^>]*class="product-title"[^>]*>([^<]+)</h1>', content)
        price_match = re.search(r'<span class="currency">[^<]+</span>([\d.]+)', content)
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        link_match = re.search(r'href="(https://www\.amazon\.ae/dp/[^"]+)"', content)
        id_match = re.search(r'كود المنتج: (\d+)', content)
        
        if title_match and price_match and image_match and link_match and id_match:
            products.append({
                'id': int(id_match.group(1)),
                'title': title_match.group(1).strip(),
                'price': float(price_match.group(1)),
                'image_link': image_match.group(1),
                'affiliate_link': link_match.group(1),
                'slug': file.replace('.html', '')
            })
    except Exception as e:
        print(f"   ✗ Error processing {file}")

# حفظ الملف
output_file = os.path.join(repo_path, 'products-data.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"   ✓ Generated {len(products)} products")
print(f"   ✓ Saved to: products-data.json\n")

print("=== All Done! ===")
