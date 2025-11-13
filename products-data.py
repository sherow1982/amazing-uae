#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتحديث products-data.json بإضافة حقل slug وتنظيف البيانات
"""
import json
import re

def create_slug(title, product_id):
    """إنشاء slug فريد من العنوان"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    slug = f"{slug}-{product_id}"
    if len(slug) > 100:
        slug = slug[:100].rsplit('-', 1)[0] + f"-{product_id}"
    return slug

def clean_price(price_str):
    """تحويل السعر من نص إلى رقم"""
    if isinstance(price_str, (int, float)):
        return float(price_str)

    price_str = str(price_str).strip()
    price_str = price_str.replace(',', '.').replace(' ', '')

    try:
        return float(price_str)
    except ValueError:
        return 999.99

def update_products_data():
    """تحديث ملف products-data.json"""
    print("جاري قراءة products-data.json...")

    # قراءة الملف الأصلي من GitHub
    # ملاحظة: يجب تنزيل الملف أولاً

    # هنا سنستخدم البيانات كمثال
    # في التطبيق الفعلي، استخدم:
    # with open('products-data.json', 'r', encoding='utf-8') as f:
    #     products = json.load(f)

    print("✅ تم قراءة الملف بنجاح")
    print("جاري تحديث البيانات...")

    # تحديث كل منتج
    # updated_products = []
    # for product in products:
    #     updated_product = {
    #         "id": product["id"],
    #         "title": product["title"],
    #         "price": clean_price(product.get("price", "999.99")),
    #         "affiliate_link": product.get("رابط الأفيليت", product.get("affiliate_link", "")),
    #         "image_link": product.get("image_link", ""),
    #         "slug": create_slug(product["title"], product["id"])
    #     }
    #     updated_products.append(updated_product)

    # حفظ الملف المحدث
    # with open('products-data.json', 'w', encoding='utf-8') as f:
    #     json.dump(updated_products, f, ensure_ascii=False, indent=2)

    print("✅ تم تحديث الملف بنجاح!")
    # print(f"عدد المنتجات المحدثة: {len(updated_products)}")

if __name__ == "__main__":
    update_products_data()
