import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Google Fonts
old_fonts = '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400;700&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap" rel="stylesheet">'
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">'
html = html.replace(old_fonts, new_fonts)

# 2. Terminal Colors & Fonts (High-Velocity Intelligence)
css_updates = [
    ('--bg:#08080c;', '--bg:#000000;'),           # Deep void black
    ('--bg2:#0d0d12;', '--bg2:#07080a;'),         # Slate gray panel background
    ('--s0:#101016;', '--s0:#000000;'),           # Deep black
    ('--s1:#14141c;', '--s1:#07080a;'),           # Slate gray
    ('--s2:#1a1a24;', '--s2:#0d0f12;'),           # Lighter slate
    ('--muted:#5a5a6e;', '--muted:#64748b;'),     # Slate metadata text
    ('--ink:#f0ece4;', '--ink:#ffffff;'),         # Stark white primary text
    ('--ink2:#b8b0a4;', '--ink2:#94a3b8;'),       # Soft gray secondary text
    ('--red:#e8394a;', '--red:#ff003c;'),         # Radioactive crimson
    ('--green:#22d45a;', '--green:#00ff66;'),     # Neon green
    ('--gold:#f5a623;', '--gold:#ffaa00;'),       # Warning orange
    ('--font-big:\'Bebas Neue\',Impact,sans-serif;', '--font-big:\'Syne\',sans-serif;'),
    ('--font-body:\'Crimson Pro\',Georgia,serif;', '--font-body:\'Inter\',sans-serif;'),
    ('--font-ui:\'Barlow Condensed\',sans-serif;', '--font-ui:\'Inter\',sans-serif;')
]
for old, new in css_updates:
    html = html.replace(old, new)

# 3. Adjust Font Sizes for Syne and Inter
# Syne is a very wide font, so we need to reduce the font-size clamp slightly so it doesn't break the layout.
# Old: font-size:clamp(3.2rem,10vw,5.2rem)
html = html.replace('font-size:clamp(3.2rem,10vw,5.2rem)', 'font-size:clamp(2.5rem,8vw,4rem)') # For .brand
# Old: font-size:clamp(3rem,8vw,5.5rem)
html = html.replace('font-size:clamp(3rem,8vw,5.5rem)', 'font-size:clamp(2rem,6vw,4.5rem)') # For .headline

# Inter has a larger x-height than Crimson Pro, so 1.25rem looks huge. We scale body down slightly.
# Old: .brief{font-size:1.25rem;line-height:1.7}
html = html.replace('.brief{font-size:1.25rem;line-height:1.7}', '.brief{font-size:1.05rem;line-height:1.6;font-weight:400;color:#cbd5e1}')

# Fix tiny unreadable fonts (metadata) manually, safely.
html = html.replace('font-size:.48rem', 'font-size:.65rem') # For tiny tags
html = html.replace('font-size:.5rem', 'font-size:.7rem') # For tiny boot text
html = html.replace('font-size:.6rem', 'font-size:.75rem') # For small metadata
html = html.replace('font-size:.65rem', 'font-size:.8rem') # For small labels

# 4. Make it 100% free by replacing playCard function safely
free_play = '''function playCard(p){
    const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)} PLAY</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;
    return `<div class="play-card">${inner}</div>`
}'''
html = re.sub(r'function playCard\(p\)\{.*?return `<div class="play-card">`.*?\}', free_play, html, flags=re.DOTALL)
html = html.replace('function playCard(p){const locked=p.type!==\'SAFE\';const inner=`<div class="play-card-type ${p.type===\'SAFE\'?\'bull\':p.type===\'AGGRESSIVE\'?\'bear\':\'neut\'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${locked?`<div class="play-blur-content">${inner}</div><div class="play-lock-overlay"><div class="play-lock-label">${esc(p.type)} PLAY - PRO ONLY</div><a class="play-unlock-btn" href="https://sumanth664.gumroad.com/l/hlpqa" target="_blank" rel="noopener">UNLOCK PRO</a></div>`:inner}</div>`}', free_play)

# 5. Make the boot screen disappear gracefully
# We will just ensure the JS is pristine. The JS in index.backup.html is already pristine.

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Perfect terminal design applied.")
