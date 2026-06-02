import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CLEAN FONT SCALING
# Instead of regex replacing every rem, we increase the root font size by 20%
# This makes .48rem look like .58rem, and 1rem look like 1.2rem. Perfect proportional scaling.
html = html.replace('html{scroll-behavior:smooth}', 'html{scroll-behavior:smooth; font-size: 125%;}')

# 2. CLEAN COLOR CONTRAST
# Brightening text without changing the hue.
html = html.replace('--ink:#f0ece4;', '--ink:#ffffff;')
html = html.replace('--ink2:#b8b0a4;', '--ink2:#d4cfc5;')
html = html.replace('--muted:#5a5a6e;', '--muted:#8b8b9d;')
html = html.replace('--dim:#28283a;', '--dim:#424252;')

# 3. 100% FREE (REMOVE GUMROAD, KEEP DESIGN CLEAN)
free_play = '''function playCard(p){
    const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)} PLAY</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;
    return `<div class="play-card">${inner}</div>`
}'''
html = re.sub(r'function playCard\(p\)\{.*?return `<div class="play-card">`.*?\}', free_play, html, flags=re.DOTALL)
html = html.replace('function playCard(p){const locked=p.type!==\'SAFE\';const inner=`<div class="play-card-type ${p.type===\'SAFE\'?\'bull\':p.type===\'AGGRESSIVE\'?\'bear\':\'neut\'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${locked?`<div class="play-blur-content">${inner}</div><div class="play-lock-overlay"><div class="play-lock-label">${esc(p.type)} PLAY - PRO ONLY</div><a class="play-unlock-btn" href="https://sumanth664.gumroad.com/l/hlpqa" target="_blank" rel="noopener">UNLOCK PRO</a></div>`:inner}</div>`}', free_play)

# 4. AUDIO PERSONALITIES (Cleanly injected)
start_idx = html.find('function chaosSpeak(paneId,btn){')
end_idx = html.find('function copyLine(){')

if start_idx != -1 and end_idx != -1:
    correct_audio_js = '''function chaosSpeak(paneId,btn){
    if(!('speechSynthesis' in window))return;
    if(btn.classList.contains('playing')){speechSynthesis.cancel();btn.classList.remove('playing');btn.textContent='LISTEN';return}
    document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='LISTEN'});
    const text=document.getElementById(paneId)?.innerText.replace(/\\s+/g,' ').trim();
    if(!text)return;
    const u=new SpeechSynthesisUtterance(text);
    u.lang='en-US';
    if(paneId.includes('eli5')){ u.rate=1.15; u.pitch=1.2; }
    else if(paneId.includes('quant')){ u.rate=0.9; u.pitch=0.75; }
    else { u.rate=1.0; u.pitch=1.0; }
    btn.classList.add('playing');btn.textContent='PLAYING';
    u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};
    speechSynthesis.cancel();speechSynthesis.speak(u);
}
'''
    html = html[:start_idx] + correct_audio_js + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied clean, professional UI fixes.")
