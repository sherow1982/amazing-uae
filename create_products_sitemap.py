import os
import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

repo = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'
base_url = 'https://amazing-uae.arabsad.com'

# قراءة المنتجات
with open(os.path.join(repo, 'products-data.json'), 'r', encoding='utf-8') as f:
    products = json.load(f)

# إنشاء products-sitemap.xml
urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

for product in products:
    url = SubElement(urlset, 'url')
    SubElement(url, 'loc').text = f"{base_url}/products/{product['slug']}.html"
    SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
    SubElement(url, 'changefreq').text = 'weekly'
    SubElement(url, 'priority').text = '0.8'

xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
with open(os.path.join(repo, 'products-sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(xml_str)

print(f"✅ تم إنشاء products-sitemap.xml بنجاح!")
print(f"   عدد المنتجات: {len(products)}")
print(f"\nالرابط: {base_url}/products-sitemap.xml")
