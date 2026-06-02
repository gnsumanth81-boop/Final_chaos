def unlock_plays():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    original_func = """function playCard(p){const locked=p.type!=='SAFE';const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${locked?`<div class="play-blur-content">${inner}</div><div class="play-lock-overlay"><div class="play-lock-label">${esc(p.type)} PLAY - PRO ONLY</div><a class="play-unlock-btn" href="https://sumanth664.gumroad.com/l/hlpqa" target="_blank" rel="noopener">UNLOCK PRO</a></div>`:inner}</div>`}"""
    
    unlocked_func = """function playCard(p){const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${inner}</div>`}"""

    if original_func in html:
        html = html.replace(original_func, unlocked_func)
        with open('public/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Cleanly replaced playCard function with unlocked version!")
    else:
        print("ERROR: Could not find original function in index.html")

unlock_plays()
