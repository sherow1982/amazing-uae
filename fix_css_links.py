import os
import re

# مسار المجلد الرئيسي للريبو
repo_path = r'C:\Users\shero\OneDrive\Desktop\amazing-uae'

# قائمة بجميع ملفات HTML في المجلد والمجلدات الفرعية
html_files = []
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files")

# نمط البحث عن السطر الذي يحتوي على style.css
pattern = r'<link\s+rel="stylesheet"\s+href="[^"]*style\.css[^"]*">'

# عداد للملفات المعدلة
modified_count = 0

for html_file in html_files:
    try:
        # قراءة محتوى الملف
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن السطر
        if re.search(pattern, content):
            # تعليق السطر
            new_content = re.sub(pattern, r'<!-- \g<0> -->', content)
            
            # كتابة المحتوى المعدل
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            modified_count += 1
            print(f"✓ Modified: {os.path.basename(html_file)}")
    
    except Exception as e:
        print(f"✗ Error processing {html_file}: {str(e)}")

print(f"\n✓ Done! Modified {modified_count} files")
