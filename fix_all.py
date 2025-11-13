import os
import re
import json
import shutil

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
products_dir = os.path.join(repo, 'products')

print("🔧 Complete Fix Started...\n")

# 1. إعادة تسمية ملفات المنتجات (إزالة / والمسافات)
print("1. Renaming product files...")
renamed = 0
file_mapping = {}

for filename in os.listdir(products_dir):
    if not filename.endswith('.html'):
        continue
    
    # تنظيف اسم الملف
    new_name = filename
    new_name = new_name.replace('/', '-')  # استبدال / بـ -
    new_name = re.sub(r'[^\w\-.]', '-', new_name)  # إزالة أحرف خاصة
    new_name = re.sub(r'-+', '-', new_name)  # دمج - المتكررة
    new_name = new_name[:150] + '.html' if len(new_name) > 150 else new_name  # تقصير الاسم
    
    if filename != new_name:
        old_path = os.path.join(products_dir, filename)
        new_path = os.path.join(products_dir, new_name)
        os.rename(old_path, new_path)
        file_mapping[filename] = new_name
        renamed += 1

print(f"   ✓ Renamed {renamed} files\n")

# 2. حذف روابط style.css
print("2. Removing style.css links...")
fixed = 0
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
                fixed += 1

print(f"   ✓ Fixed {fixed} files\n")

# 3. توليد products-data.json
print("3. Generating products-data.json...")
products = []

for filename in os.listdir(products_dir):
    if not filename.endswith('.html'):
        continue
    
    try:
        filepath = os.path.join(products_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        title = re.search(r'<h1[^>]*class="product-title"[^>]*>([^<]+)</h1>', html)
        price = re.search(r'<span class="currency">[^<]*</span>([\d.]+)', html)
        image = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        link = re.search(r'href="(https://www\.amazon\.ae/dp/[^"]+)"', html)
        prod_id = re.search(r'كود المنتج: (\d+)', html)
        
        if all([title, price, image, link, prod_id]):
            products.append({
                'id': int(prod_id.group(1)),
                'title': title.group(1).strip(),
                'price': float(price.group(1)),
                'image_link': image.group(1),
                'affiliate_link': link.group(1),
                'slug': filename.replace('.html', '')
            })
    except Exception as e:
        print(f"   ⚠ Error: {filename}")

output = os.path.join(repo, 'products-data.json')
with open(output, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"   ✓ Generated {len(products)} products\n")

print("✅ All Done!\n")
print("📤 Now push to GitHub:")
print("   git add .")
print('   git commit -m "Fix product URLs and errors"')
print("   git push")
