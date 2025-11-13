import os

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
index_path = os.path.join(repo, 'index.html')

new_index = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazing UAE - أفضل المنتجات من أمازون الإمارات</title>
    <meta name="description" content="اكتشف أفضل المنتجات والعروض الحصرية من أمازون الإمارات بأسعار تنافسية. تسوق الآن واحصل على أفضل الصفقات">
    <meta name="keywords" content="أمازون الإمارات, تسوق أونلاين, منتجات أمازون, عروض أمازون, تسوق الإمارات">
    <link rel="canonical" href="https://sherow1982.github.io/amazing-uae/">
    <meta property="og:title" content="Amazing UAE - أفضل المنتجات من أمازون الإمارات">
    <meta property="og:description" content="اكتشف أفضل المنتجات والعروض من أمازون الإمارات">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://sherow1982.github.io/amazing-uae/">
    <style>
        * {margin:0;padding:0;box-sizing:border-box;}
        body {font-family:'Segoe UI',Tahoma,Verdana,sans-serif;background:#f5f5f5;}
        header {background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:2rem;text-align:center;}
        h1 {font-size:2.5rem;margin-bottom:.5rem;}
        .container {max-width:1400px;margin:2rem auto;padding:0 1rem;}
        #products-grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:2rem;margin-top:2rem;}
        .product-card {background:white;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1);transition:transform .3s,box-shadow .3s;cursor:pointer;}
        .product-card:hover {transform:translateY(-5px);box-shadow:0 8px 16px rgba(0,0,0,.2);}
        .product-link {display:block;text-decoration:none;color:inherit;}
        .product-card img {width:100%;height:280px;object-fit:contain;background:#fafafa;padding:1rem;}
        .product-card img.lazy {opacity:0;transition:opacity .3s;}
        .product-card img.loaded {opacity:1;}
        .product-title {padding:1rem;font-size:.95rem;line-height:1.4;min-height:80px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
        .product-price {padding:0 1rem;font-size:1.3rem;font-weight:bold;color:#667eea;}
        .view-more-btn {display:block;background:#667eea;color:white;text-align:center;padding:.6rem;margin:.5rem 1rem 1rem;text-decoration:none;font-weight:500;border-radius:6px;transition:background .3s;}
        .view-more-btn:hover {background:#5568d3;}
        .amazon-btn {display:block;background:#ff9900;color:white;text-align:center;padding:.8rem;margin:0 1rem 1rem;text-decoration:none;font-weight:bold;border-radius:6px;transition:background .3s;}
        .amazon-btn:hover {background:#e88b00;}
        .loading {text-align:center;padding:3rem;font-size:1.2rem;color:#667eea;}
        .load-more-container {text-align:center;margin:3rem 0;}
        .load-more-btn {background:#667eea;color:white;border:none;padding:1rem 3rem;font-size:1.1rem;font-weight:bold;border-radius:8px;cursor:pointer;transition:background .3s;}
        .load-more-btn:hover {background:#5568d3;}
        .load-more-btn:disabled {background:#ccc;cursor:not-allowed;}
        footer {background:#333;color:white;text-align:center;padding:2rem;margin-top:4rem;}
        @media (max-width:768px){#products-grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1rem;}.product-card img{height:200px;}h1{font-size:1.8rem;}}
    </style>
</head>
<body>
    <header>
        <h1>🛍️ Amazing UAE</h1>
        <p>أفضل المنتجات من أمازون الإمارات</p>
    </header>
    <div class="container">
        <div id="products-grid">
            <div class="loading">جاري تحميل المنتجات...</div>
        </div>
        <div class="load-more-container" id="load-more-container" style="display:none;">
            <button class="load-more-btn" id="load-more-btn">تحميل المزيد من المنتجات</button>
        </div>
    </div>
    <footer>
        <p>&copy; 2024 Amazing UAE - جميع الحقوق محفوظة</p>
    </footer>
    <script>
        let allProducts = [];
        let displayedCount = 0;
        const productsPerPage = 20;

        const lazyLoadImage = (img) => {
            const src = img.dataset.src;
            if (src) {
                img.src = src;
                img.classList.add('loaded');
                img.removeAttribute('data-src');
            }
        };

        const observeImages = () => {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        lazyLoadImage(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            });
            document.querySelectorAll('img.lazy').forEach(img => {
                imageObserver.observe(img);
            });
        };

        const loadMoreProducts = () => {
            const grid = document.getElementById('products-grid');
            const endIndex = Math.min(displayedCount + productsPerPage, allProducts.length);
            for (let i = displayedCount; i < endIndex; i++) {
                const product = allProducts[i];
                const productUrl = `products/${product.slug}.html`;
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <a href="${productUrl}" class="product-link" title="عرض تفاصيل ${product.title}">
                        <img class="lazy" data-src="${product.image_link}" alt="${product.title}" width="280" height="280">
                        <div class="product-title">${product.title}</div>
                        <div class="product-price">${product.price} درهم</div>
                    </a>
                    <a href="${productUrl}" class="view-more-btn">شاهد المزيد</a>
                    <a href="${product.affiliate_link}" class="amazon-btn" target="_blank" rel="nofollow noopener">اشتري من أمازون</a>
                `;
                grid.appendChild(card);
            }
            displayedCount = endIndex;
            observeImages();
            if (displayedCount >= allProducts.length) {
                document.getElementById('load-more-container').style.display = 'none';
            }
        };

        fetch('products-data.json')
            .then(response => response.json())
            .then(products => {
                allProducts = products;
                const grid = document.getElementById('products-grid');
                grid.innerHTML = '';
                loadMoreProducts();
                if (allProducts.length > productsPerPage) {
                    document.getElementById('load-more-container').style.display = 'block';
                }
                document.getElementById('load-more-btn').addEventListener('click', loadMoreProducts);
            })
            .catch(error => {
                document.getElementById('products-grid').innerHTML = '<div class="loading">حدث خطأ في تحميل المنتجات</div>';
            });
    </script>
</body>
</html>'''

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_index)

print("✅ تم تحديث index.html بنجاح!")
print("\nالآن:")
print("  git add index.html")
print('  git commit -m "Fix product links in index"')
print("  git push")
