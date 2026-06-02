html = open('public/index.html', encoding='utf-8').read()
html = html.replace('\\n', '\n')
open('public/index.html', 'w', encoding='utf-8').write(html)
print("Replaced literal backslash n with newline")
