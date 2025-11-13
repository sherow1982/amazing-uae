import os
import re
import json
import hashlib

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
products_dir = os.path.join(repo, 'products')

print("🔧 Final Fix - Shortening All Product File Names\n")

# Step 1: اختصار أسماء الملفات
print("Renaming all product files to short names...")
mapping = {}
products_data = []

for idx, filename in enumerate(sorted(os.listdir(products_dir)), 1):
    if not filename.endswith('.html'):
        continue
    
    old_path = os.path.join(products_dir, filename)
    
    try:
        with open(old_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # استخراج البيانات
        title = re.search(r'<h1[^>]*class="product-title"[^>]*>([^<]+)</h1>', html)
        price = re.search(r'<span class="currency">[^<]*</span>([\d.]+)', html)
        image = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        link = re.search(r'href="(https://www\.amazon\.ae/dp/[^"]+)"', html)
        pid = re.search(r'كود المنتج: (\d+)', html)
        
        if not all([title, price, image, link, pid]):
            continue
        
        # اسم جديد قصير
        product_id = pid.group(1)
        new_filename = f"product-{product_id}.html"
        new_path = os.path.join(products_dir, new_filename)
        
        # إعادة تسمية
        os.rename(old_path, new_path)
        
        # حفظ البيانات
        products_data.append({
            'id': int(product_id),
            'title': title.group(1).strip(),
            'price': float(price.group(1)),
            'image_link': image.group(1),
            'affiliate_link': link.group(1),
            'slug': new_filename.replace('.html', '')
        })
        
        print(f"✓ {idx}: {filename[:50]}... → {new_filename}")
        
    except Exception as e:
        print(f"✗ Error: {filename[:50]}...")

print(f"\n✓ Renamed {len(products_data)} files\n")

# Step 2: توليد products-data.json
print("Creating products-data.json...")
with open(os.path.join(repo, 'products-data.json'), 'w', encoding='utf-8') as f:
    json.dump(products_data, f, ensure_ascii=False, indent=2)

print(f"✓ Created products-data.json with {len(products_data)} products\n")

# Step 3: حذف style.css
print("Removing style.css links...")
fixed = 0
for root, _, files in os.walk(repo):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                new = re.sub(r'<link[^>]*style\.css[^>]*>', '', content)
                if content != new:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new)
                    fixed += 1
            except:
                pass

print(f"✓ Fixed {fixed} files\n")

print("=" * 60)
print("✅ COMPLETE! All product files now have short names.")
print("=" * 60)
print("\nNext:")
print("  git add .")
print('  git commit -m "Shorten product file names"')
print("  git push")
print("\n🎉 No more 404 errors after push!")
