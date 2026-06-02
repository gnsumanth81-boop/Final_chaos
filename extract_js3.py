import re
with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if match:
    with open('temp.js', 'w', encoding='utf-8') as out:
        out.write(match.group(1))
