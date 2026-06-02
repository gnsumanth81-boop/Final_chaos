import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Google Fonts
old_fonts = '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400;700&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap" rel="stylesheet">'
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">'
html = html.replace(old_fonts, new_fonts)

# 2. Update CSS Variables for Fonts and Colors
css_updates = [
    ('--bg:#08080c;', '--bg:#07080a;'),
    ('--bg2:#0d0d12;', '--bg2:#0d0f12;'),
    ('--s0:#101016;', '--s0:#000000;'),
    ('--s1:#14141c;', '--s1:#07080a;'),
    ('--s2:#1a1a24;', '--s2:#0d0f12;'),
    ('--muted:#5a5a6e;', '--muted:#64748b;'),
    ('--muted:#8b8b9d;', '--muted:#64748b;'),
    ('--dim:#28283a;', '--dim:#1f2937;'),
    ('--dim:#424252;', '--dim:#1f2937;'),
    ('--red:#e8394a;', '--red:#ff003c;'),
    ('--red-g:rgba(232,57,74,.12);', '--red-g:rgba(255,0,60,.12);'),
    ('--green:#22d45a;', '--green:#00ff66;'),
    ('--green-g:rgba(34,212,90,.1);', '--green-g:rgba(0,255,102,.1);'),
    ('--gold:#f5a623;', '--gold:#ffaa00;'),
    ('--gold-g:rgba(245,166,35,.1);', '--gold-g:rgba(255,170,0,.1);'),
    ("--font-big:'Bebas Neue',Impact,sans-serif;", "--font-big:'Syne',sans-serif;"),
    ("--font-body:'Crimson Pro',Georgia,serif;", "--font-body:'Inter',sans-serif;"),
    ("--font-ui:'Barlow Condensed',sans-serif;", "--font-ui:'Inter',sans-serif;")
]

for old, new in css_updates:
    html = html.replace(old, new)

# 3. Fix line height and font weights for the new Syne font
html = re.sub(r'\.brand\{.*?\}', '.brand{font-family:var(--font-big);font-size:clamp(3.2rem,10vw,5.2rem);letter-spacing:-1px;line-height:1;font-weight:800;color:var(--ink)}', html)
html = re.sub(r'\.headline\{.*?\}', '.headline{font-family:var(--font-big);font-weight:800;font-size:clamp(3rem,8vw,5.5rem);line-height:1.1;letter-spacing:-1px;text-transform:uppercase;color:var(--ink);text-shadow:0 0 40px rgba(255,255,255,.1);margin-bottom:20px}', html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied High-Velocity Intelligence Design System")
