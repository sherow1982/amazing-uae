
import json
import re

# قراءة products-data.json
with open('products-data.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

def create_filename(title, product_id):
    """تحويل title إلى filename صحيح"""
    # تحويل لأحرف صغيرة
    filename = title.lower()
    # إزالة الرموز الخاصة واستبدالها بـ -
    filename = re.sub(r'[^\w\s؀-ۿ-]', '', filename)
    # استبدال المسافات بـ -
    filename = re.sub(r'\s+', '-', filename)
    # إزالة - المتكررة
    filename = re.sub(r'-+', '-', filename)
    # إزالة - من البداية والنهاية
    filename = filename.strip('-')
    # قص الاسم إذا كان طويل جداً (أقصى 100 حرف)
    if len(filename) > 100:
        filename = filename[:100].rsplit('-', 1)[0]
    # إضافة ID والامتداد
    return f"{filename}-{product_id}.html"

# إضافة filename لكل منتج
for product in products:
    product_id = product.get('id', '')
    title = product.get('title', '')
    product['filename'] = create_filename(title, product_id)

# حفظ الملف المحدث
with open('products-data-updated.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f"✓ تم تحديث {len(products)} منتج")
print("الملف الجديد: products-data-updated.json")
