import os
import re
import json

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
products_dir = os.path.join(repo, 'products')

print("🔧 Fixing Repository...\n")

# 1. حذف style.css links
count = 0
for root, _, files in os.walk(repo):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = re.sub(r'<link[^>]*style\.css[^>]*>\s*', '', content)
            
            if content != new_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1

print(f"✓ Removed style.css from {count} files")

# 2. توليد products-data.json
products = []
for f in os.listdir(products_dir):
    if not f.endswith('.html'):
        continue
    
    try:
        with open(os.path.join(products_dir, f), 'r', encoding='utf-8') as file:
            html = file.read()
        
        matches = {
            'title': re.search(r'<h1[^>]*class="product-title"[^>]*>([^<]+)</h1>', html),
            'price': re.search(r'<span class="currency">[^<]*</span>([\d.]+)', html),
            'image': re.search(r'<meta property="og:image" content="([^"]+)"', html),
            'link': re.search(r'href="(https://www\.amazon\.ae/dp/[^"]+)"', html),
            'id': re.search(r'كود المنتج: (\d+)', html)
        }
        
        if all(matches.values()):
            products.append({
                'id': int(matches['id'].group(1)),
                'title': matches['title'].group(1).strip(),
                'price': float(matches['price'].group(1)),
                'image_link': matches['image'].group(1),
                'affiliate_link': matches['link'].group(1),
                'slug': f.replace('.html', '')
            })
    except:
        continue

with open(os.path.join(repo, 'products-data.json'), 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"✓ Generated {len(products)} products in products-data.json")
print("\n✅ Done! Now run:")
print("   git add .")
print('   git commit -m "Fix errors"')
print("   git push")
