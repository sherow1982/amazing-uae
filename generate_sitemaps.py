import os
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
base_url = 'https://amazing-uae.arabsad.com'

print("🔧 Generating Sitemaps and Merchant Feed...\n")

# 1. قراءة بيانات المنتجات
with open(os.path.join(repo, 'products-data.json'), 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"✓ Loaded {len(products)} products\n")

# 2. إنشاء Sitemap رئيسي
print("Creating main sitemap.xml...")
urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# الصفحة الرئيسية
url = SubElement(urlset, 'url')
SubElement(url, 'loc').text = base_url + '/'
SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
SubElement(url, 'changefreq').text = 'daily'
SubElement(url, 'priority').text = '1.0'

# حفظ sitemap.xml
xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
with open(os.path.join(repo, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("✓ Created sitemap.xml\n")

# 3. إنشاء Products Sitemap
print("Creating products-sitemap.xml...")
urlset_products = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

for product in products:
    url = SubElement(urlset_products, 'url')
    SubElement(url, 'loc').text = f"{base_url}/products/{product['slug']}.html"
    SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    SubElement(url, 'changefreq').text = 'weekly'
    SubElement(url, 'priority').text = '0.8'

xml_str = minidom.parseString(tostring(urlset_products)).toprettyxml(indent="  ")
with open(os.path.join(repo, 'products-sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("✓ Created products-sitemap.xml\n")

# 4. إنشاء Google Merchant Feed
print("Creating google_merchant_feed.xml...")
rss = Element('rss', version="2.0", attrib={
    'xmlns:g': 'http://base.google.com/ns/1.0'
})
channel = SubElement(rss, 'channel')
SubElement(channel, 'title').text = 'Amazing UAE Products'
SubElement(channel, 'link').text = base_url
SubElement(channel, 'description').text = 'أفضل المنتجات من أمازون الإمارات'

for product in products:
    item = SubElement(channel, 'item')
    SubElement(item, '{http://base.google.com/ns/1.0}id').text = str(product['id'])
    SubElement(item, '{http://base.google.com/ns/1.0}title').text = product['title'][:150]
    SubElement(item, '{http://base.google.com/ns/1.0}description').text = product['title']
    SubElement(item, '{http://base.google.com/ns/1.0}link').text = f"{base_url}/products/{product['slug']}.html"
    SubElement(item, '{http://base.google.com/ns/1.0}image_link').text = product['image_link']
    SubElement(item, '{http://base.google.com/ns/1.0}condition').text = 'new'
    SubElement(item, '{http://base.google.com/ns/1.0}availability').text = 'in stock'
    SubElement(item, '{http://base.google.com/ns/1.0}price').text = f"{product['price']} AED"
    SubElement(item, '{http://base.google.com/ns/1.0}brand').text = 'Amazon'
    SubElement(item, '{http://base.google.com/ns/1.0}gtin').text = str(product['id'])

xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")
with open(os.path.join(repo, 'google_merchant_feed.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("✓ Created google_merchant_feed.xml\n")

# 5. إنشاء sitemap index
print("Creating sitemap_index.xml...")
sitemapindex = Element('sitemapindex', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

sitemap1 = SubElement(sitemapindex, 'sitemap')
SubElement(sitemap1, 'loc').text = base_url + '/sitemap.xml'
SubElement(sitemap1, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')

sitemap2 = SubElement(sitemapindex, 'sitemap')
SubElement(sitemap2, 'loc').text = base_url + '/products-sitemap.xml'
SubElement(sitemap2, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')

xml_str = minidom.parseString(tostring(sitemapindex)).toprettyxml(indent="  ")
with open(os.path.join(repo, 'sitemap_index.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("✓ Created sitemap_index.xml\n")

print("=" * 60)
print("✅ All files created successfully!")
print("=" * 60)
print("\nGenerated files:")
print("  ✓ sitemap.xml")
print("  ✓ products-sitemap.xml")
print("  ✓ sitemap_index.xml")
print("  ✓ google_merchant_feed.xml")
print("\nNext steps:")
print("  1. git add .")
print('  2. git commit -m "Add sitemaps and merchant feed"')
print("  3. git push")
print("\nAfter push:")
print(f"  📤 Submit to Google Merchant Center:")
print(f"     {base_url}/google_merchant_feed.xml")
print(f"\n  📤 Submit to Google Search Console:")
print(f"     {base_url}/sitemap_index.xml")
