import json
import os
import re
from urllib.parse import quote

def create_slug(title, product_id):
    """إنشاء slug من العنوان والـ ID - يدعم العربي"""
    # تحويل لأحرف صغيرة
    slug = title.lower()
    
    # استبدال المسافات بشَرطات
    slug = re.sub(r'[\s_]+', '-', slug)
    
    # إزالة الأحرف الخاصة فقط (يبقي على العربي والإنجليزي والأرقام)
    slug = re.sub(r'[^\w\u0600-\u06FF-]', '', slug)
    
    # إزالة الشرطات المتعددة
    slug = re.sub(r'-+', '-', slug)
    
    # قص النص للطول المناسب وإزالة الشرطات من البداية والنهاية
    slug = slug[:80].strip('-')
    
    # إضافة الـ ID في النهاية
    return f"{slug}-{product_id}"

# قراءة كل المنتجات من ملف JSON
print("📂 قراءة ملف products-data.json...")
with open('products-data.json', encoding='utf-8') as f:
    products = json.load(f)

print(f"✅ تم العثور على {len(products)} منتج")

# قالب صفحة المنتج HTML الكامل
template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | متجر الإمارات المذهل</title>
    <meta name="description" content="{title} - اشتري الآن بأفضل سعر {price} درهم">
    <meta name="keywords" content="{title}, تسوق اونلاين, الإمارات, أمازون">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image}">
    <meta property="og:type" content="product">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .navbar {{ 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{ 
            color: white; 
            font-size: 24px; 
            font-weight: bold; 
            text-decoration: none;
        }}
        .nav-links {{ 
            list-style: none; 
            display: flex; 
            gap: 25px; 
        }}
        .nav-links a {{ 
            color: white; 
            text-decoration: none; 
            font-weight: 500;
            transition: all 0.3s;
            padding: 8px 16px;
            border-radius: 8px;
        }}
        .nav-links a:hover {{
            background: rgba(255,255,255,0.2);
        }}
        .breadcrumb {{ 
            padding: 20px 30px; 
            font-size: 14px; 
            color: #666;
            background: #f8f9fa;
        }}
        .breadcrumb a {{ 
            color: #667eea; 
            text-decoration: none; 
            margin: 0 5px;
        }}
        .product-container {{
            padding: 40px 30px;
        }}
        .product-details {{ 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 50px;
        }}
        .product-gallery {{
            position: sticky;
            top: 20px;
            height: fit-content;
        }}
        .main-image {{ 
            width: 100%; 
            border: 2px solid #e0e0e0;
            border-radius: 16px; 
            overflow: hidden;
            background: white;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .main-image img {{ 
            width: 100%; 
            height: auto; 
            display: block;
        }}
        .product-info {{ 
            display: flex; 
            flex-direction: column; 
            gap: 25px;
        }}
        .product-title {{ 
            font-size: 32px; 
            font-weight: 700; 
            color: #1a1a1a;
            line-height: 1.4;
        }}
        .product-id {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        .product-price-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 16px;
            color: white;
        }}
        .price-label {{
            font-size: 16px;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        .current-price {{ 
            font-size: 42px; 
            font-weight: 700;
            display: block;
        }}
        .currency {{
            font-size: 24px;
            margin-right: 5px;
        }}
        .product-description {{ 
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            line-height: 1.8; 
            color: #555;
        }}
        .product-description h2 {{
            font-size: 20px;
            margin-bottom: 15px;
            color: #333;
        }}
        .product-actions {{ 
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 30px;
        }}
        .btn {{ 
            padding: 18px 35px; 
            font-size: 18px; 
            font-weight: 600; 
            border: none; 
            border-radius: 12px; 
            cursor: pointer; 
            text-decoration: none; 
            text-align: center; 
            transition: all 0.3s;
            display: block;
        }}
        .btn-primary {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }}
        .btn-primary:hover {{ 
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
        }}
        .btn-amazon {{ 
            background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%);
            color: white;
            box-shadow: 0 10px 25px rgba(255, 153, 0, 0.4);
        }}
        .btn-amazon:hover {{ 
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(255, 153, 0, 0.6);
        }}
        footer {{ 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white; 
            text-align: center; 
            padding: 30px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 0; }}
            .container {{ border-radius: 0; }}
            .product-details {{ 
                grid-template-columns: 1fr; 
                gap: 30px;
            }}
            .product-title {{ font-size: 24px; }}
            .current-price {{ font-size: 32px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <nav class="navbar">
                <a href="../index.html" class="logo">🛍️ متجر الإمارات المذهل</a>
                <ul class="nav-links">
                    <li><a href="../index.html">🏠 الرئيسية</a></li>
                    <li><a href="../products.html">📦 المنتجات</a></li>
                    <li><a href="../cart.html">🛒 السلة</a></li>
                </ul>
            </nav>
        </header>

        <div class="breadcrumb">
            <a href="../index.html">الرئيسية</a> /
            <a href="../products.html">المنتجات</a> /
            <span>{title}</span>
        </div>

        <div class="product-container">
            <div class="product-details">
                <div class="product-gallery">
                    <div class="main-image">
                        <img src="{image}" alt="{title}" loading="lazy">
                    </div>
                </div>

                <div class="product-info">
                    <div>
                        <span class="product-id">كود المنتج: {product_id}</span>
                    </div>
                    
                    <h1 class="product-title">{title}</h1>

                    <div class="product-price-section">
                        <div class="price-label">السعر</div>
                        <span class="current-price">
                            <span class="currency">د.إ</span>{price}
                        </span>
                    </div>

                    <div class="product-description">
                        <h2>📝 وصف المنتج</h2>
                        <p>{description}</p>
                    </div>

                    <div class="product-actions">
                        <button class="btn btn-primary" onclick="addToCart({product_id})">
                            🛒 إضافة إلى السلة
                        </button>
                        <a href="{affiliate_link}" 
                           class="btn btn-amazon" 
                           target="_blank" 
                           rel="nofollow noopener">
                            🛍️ اشتري من أمازون
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2025 متجر الإمارات المذهل - جميع الحقوق محفوظة</p>
        </footer>
    </div>

    <script>
        function addToCart(productId) {{
            let cart = JSON.parse(localStorage.getItem('amazing_uae_cart')) || [];
            
            const product = {{
                id: {product_id},
                title: "{title}",
                price: {price},
                image: "{image}",
                affiliateLink: "{affiliate_link}",
                quantity: 1
            }};
            
            const existingProduct = cart.find(item => item.id === productId);
            
            if (existingProduct) {{
                existingProduct.quantity++;
                alert('✓ تم زيادة الكمية في السلة!');
            }} else {{
                cart.push(product);
                alert('✓ تمت إضافة المنتج للسلة بنجاح!');
            }}
            
            localStorage.setItem('amazing_uae_cart', JSON.stringify(cart));
        }}
    </script>
</body>
</html>"""

# تأكد أن مجلد products موجود
os.makedirs('products', exist_ok=True)

# عداد الملفات المولدة
count = 0

# توليد صفحات المنتجات
print("\n🔨 بدء توليد صفحات المنتجات بـ slug عربي...")
for product in products:
    try:
        # إنشاء slug عربي
        slug = product.get("slug") or create_slug(product.get('title', 'product'), product.get('id', 0))
        
        # تجهيز البيانات
        title = product.get('title', 'منتج بدون عنوان')
        price = product.get('price', 0)
        description = product.get('description', title)
        image = product.get('image_link', '')
        product_id = product.get('id', 0)
        
        # استخدام رابط الأفلييت أو الرابط العادي
        affiliate_link = product.get('affiliate_link') or product.get('link') or '#'
        
        # توليد HTML
        html_code = template.format(
            title=title,
            price=price,
            description=description,
            image=image,
            product_id=product_id,
            affiliate_link=affiliate_link
        )
        
        # حفظ الملف
        filename = f'products/{slug}.html'
        with open(filename, 'w', encoding='utf-8') as out:
            out.write(html_code)
        
        count += 1
        
        # طباعة تقدم العملية كل 100 منتج
        if count % 100 == 0:
            print(f"  ✓ تم توليد {count} صفحة...")
            
    except Exception as e:
        print(f"  ⚠️ خطأ في معالجة المنتج {product.get('id', 'unknown')}: {str(e)}")
        continue

print(f"\n✅ تم بنجاح! تم توليد {count} صفحة منتج بـ slug عربي")
print(f"📁 الملفات محفوظة في مجلد: products/")
print(f"\n⚠️ ملاحظة: GitHub Pages قد يحتاج URL encoding للأسماء العربية")
print("\n🎉 العملية اكتملت بنجاح!")
