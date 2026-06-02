with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('--ink:#f0ece4;', '--ink:#ffffff;')
html = html.replace('--ink2:#b8b0a4;', '--ink2:#e0dbd1;')
html = html.replace('--muted:#5a5a6e;', '--muted:#9c9cb4;')
html = html.replace('--dim:#28283a;', '--dim:#4a4a5f;')

# Let's also make sure any dark blue/grey text specifically set is brightened
html = html.replace('color:var(--muted)', 'color:#b0b0c5')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated colors for better contrast')
