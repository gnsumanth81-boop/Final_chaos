import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the locked playCard function with an unlocked one
unlocked_play = '''function playCard(p){const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${inner}</div>`}'''

html = re.sub(r'function playCard\(p\)\{.*?return `<div class="play-card">`.*?\+\?.*?\}', unlocked_play, html, flags=re.DOTALL)
html = re.sub(r'function playCard\(p\)\{const locked=p\.type!==\'SAFE\';const inner=.*?\}', unlocked_play, html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Removed PRO ONLY locks!")
