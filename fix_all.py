import os
import re
import json

repo_path = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
products_dir = os.path.join(repo_path, 'products')

print("=== Fixing Amazing UAE Repository ===\n")

# 1. إزالة روابط style.css
print("1. Removing style.css links...")
modified = 0
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '<link' in content and 'style.css' in content:
                    content = re.sub(r'<link[^>]*style\.css[^>]*>', '', content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    modified += 1
            except: pass

print(f"   ✓ Modified {modified} files\n")

# 2. توليد products-data.json صحيح
print("2. Generating products-data.json...")
products = []
files = [f for f in os.listdir(products_dir) if f.endswith('.html')]

for file in files:
    try:
        with open(os.path.join(products_dir, file), 'r', encoding='utf-8') as f:
            html = f.read()
        
        title = re.search(r'<h1[^>]*class="product-title"[^>]*>([^<]+)</h1>', html)
        price = re.search(r'<span class="currency">[^<]*</span>([\d.]+)', html)
        image = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        link = re.search(r'href="(https://www\.amazon\.ae/dp/[^"]+)"', html)
        pid = re.search(r'كود المنتج: (\d+)', html)
        
        if all([title, price, image, link, pid]):
            products.append({
                'id': int(pid.group(1)),
                'title': title.group(1).strip(),
                'price': float(price.group(1)),
                'image_link': image.group(1),
                'affiliate_link': link.group(1),
                'slug': file.replace('.html', '')
            })
    except: 
        pass

with open(os.path.join(repo_path, 'products-data.json'), 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"   ✓ Created products-data.json with {len(products)} products\n")

# 3. التحقق من صحة الروابط في index.html
print("3. Verifying index.html...")
index_path = os.path.join(repo_path, 'index.html')
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التأكد من وجود products-data.json
    if 'products-data.json' in content:
        print("   ✓ index.html correctly references products-data.json")
    else:
        print("   ⚠ Warning: index.html may need manual check")
else:
    print("   ✗ index.html not found")

print("\n=== Done! Now commit and push to GitHub ===")
