import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. BUMP FONTS (CAREFULLY)
# We only want to match decimals that have NO digits before the decimal point, 
# or 0 before the decimal point, e.g. .48rem or 0.48rem
def scale_small_rem(match):
    num_str = match.group(1)
    if num_str.startswith('.'):
        val = float('0' + num_str)
    else:
        val = float(num_str)
    
    # Only scale up tiny fonts
    if val < 0.7:
        new_val = val + 0.35
    elif val < 1.0:
        new_val = val + 0.15
    else:
        new_val = val
        
    return f'{new_val:.2f}rem'

# Negative lookbehind to ensure we don't match the decimal part of "3.50rem"
html = re.sub(r'(?<!\d)(0?\.\d+)rem', scale_small_rem, html)

# 2. FIX COLORS FOR HIGH CONTRAST (Dark Background issue)
html = html.replace('--ink:#f0ece4;', '--ink:#ffffff;')
html = html.replace('--ink2:#b8b0a4;', '--ink2:#e0dbd1;')
html = html.replace('--muted:#5a5a6e;', '--muted:#9c9cb4;')
html = html.replace('--dim:#28283a;', '--dim:#4a4a5f;')
html = html.replace('color:var(--muted)', 'color:#b0b0c5')

# 3. FIX CUSTOM ICONS
tabs_html = '''<div class="cx-tabs" role="tablist">
          <button class="cx-btn" onclick="setCx('eli5',this)">
            <img src="icon-eli5.png" style="width:32px;height:32px;margin-bottom:8px;border-radius:8px;box-shadow:0 0 10px rgba(255,255,255,0.2)">
            <span class="cx-n" style="font-size:1.1rem;font-weight:bold">ELI5</span><span class="cx-sub">Simple - 3 min</span>
          </button>
          <button class="cx-btn active" onclick="setCx('analyst',this)">
            <img src="icon-analyst.png" style="width:32px;height:32px;margin-bottom:8px;border-radius:8px;box-shadow:0 0 10px rgba(255,255,255,0.2)">
            <span class="cx-n" style="font-size:1.1rem;font-weight:bold">Analyst</span><span class="cx-sub">Intermediate - 5 min</span>
          </button>
          <button class="cx-btn" onclick="setCx('quant',this)">
            <img src="icon-quant.png" style="width:32px;height:32px;margin-bottom:8px;border-radius:8px;box-shadow:0 0 10px rgba(255,255,255,0.2)">
            <span class="cx-n" style="font-size:1.1rem;font-weight:bold">Quant</span><span class="cx-sub">Advanced - 7 min</span>
          </button>
        </div>'''
html = re.sub(r'<div class="cx-tabs".*?</div>', tabs_html, html, flags=re.DOTALL)

# 4. 100% FREE (REMOVE GUMROAD)
free_play = '''function playCard(p){
    const emoji=p.type==='SAFE'?'🛡️':p.type==='AGGRESSIVE'?'⚔️':'🔄';
    const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${emoji} ${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;
    return `<div class="play-card">${inner}</div>`
}'''
html = re.sub(r'function playCard\(p\)\{.*?return `<div class="play-card">`.*?\}', free_play, html, flags=re.DOTALL)
html = html.replace('function playCard(p){const locked=p.type!==\'SAFE\';const inner=`<div class="play-card-type ${p.type===\'SAFE\'?\'bull\':p.type===\'AGGRESSIVE\'?\'bear\':\'neut\'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${locked?`<div class="play-blur-content">${inner}</div><div class="play-lock-overlay"><div class="play-lock-label">${esc(p.type)} PLAY - PRO ONLY</div><a class="play-unlock-btn" href="https://sumanth664.gumroad.com/l/hlpqa" target="_blank" rel="noopener">UNLOCK PRO</a></div>`:inner}</div>`}', free_play)

# 5. BURGER MENU
css_add = '''
    /* Burger Menu */
    .burger-btn{display:none;background:0;border:0;cursor:pointer;flex-direction:column;gap:5px;padding:10px}
    .burger-line{width:25px;height:2px;background:var(--fg);transition:0.3s}
    .mobile-nav{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(10,10,12,0.95);backdrop-filter:blur(10px);z-index:999;flex-direction:column;align-items:center;justify-content:center;gap:2rem}
    .mobile-nav.open{display:flex}
    .mobile-close{position:absolute;top:20px;right:20px;background:0;border:0;color:var(--fg);font-size:2rem;cursor:pointer}
    .mobile-nav a{color:var(--ink);text-decoration:none;font-size:1.5rem;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:2px}
    @media(max-width:700px){.desktop-nav{display:none} .burger-btn{display:flex}}
    .desktop-nav{display:flex;gap:1.5rem;align-items:center}
    .desktop-nav a{color:var(--muted);text-decoration:none;font-family:var(--font-mono);font-size:1.0rem;text-transform:uppercase;letter-spacing:1px;transition:0.2s}
    .desktop-nav a:hover{color:var(--ink)}
'''
html = html.replace('</style>', css_add + '\n</style>')

burger_html = '''
  <div class="mobile-nav" id="mobile-nav">
    <button class="mobile-close" onclick="toggleMobileNav()">&times;</button>
    <a href="#" onclick="toggleMobileNav()">Dashboard</a>
    <a href="#" onclick="toggleMobileNav()">Archive</a>
    <a href="#" onclick="toggleMobileNav()">FAQ</a>
    <a href="#" onclick="toggleMobileNav()">Past Signals</a>
    <a href="https://t.me/yourchannel" target="_blank">Free Telegram</a>
  </div>
  <div class="wrap">
    <header class="hdr">
      <div class="hdr-top" style="display:flex;justify-content:space-between;align-items:center;width:100%">
        <div style="display:flex;align-items:center;gap:15px">
          <div class="brand">CHAOS<em>.</em></div><div class="live-b"><span class="live-d"></span>LIVE BRIEF</div>
        </div>
        <nav class="desktop-nav">
          <a href="#">Dashboard</a>
          <a href="#">Archive</a>
          <a href="#">FAQ</a>
          <a href="#">Past Signals</a>
          <a href="https://t.me/yourchannel" target="_blank" style="color:var(--gold)">Free Telegram</a>
        </nav>
        <button class="burger-btn" onclick="toggleMobileNav()">
          <span class="burger-line"></span><span class="burger-line"></span><span class="burger-line"></span>
        </button>
      </div>
'''
html = re.sub(r'<div class="wrap">\s*<header class="hdr">\s*<div class="hdr-top"><div class="brand">CHAOS<em>\.</em></div><div class="live-b"><span class="live-d"></span>LIVE BRIEF</div></div>', burger_html, html)

js_add = '''
    function toggleMobileNav(){
      const nav = document.getElementById('mobile-nav');
      nav.classList.toggle('open');
    }
'''
html = html.replace('<script>', '<script>\n' + js_add)

# 6. AUDIO PERSONALITIES (SAFE STRING REPLACE INSTEAD OF REGEX)
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
    if(paneId.includes('eli5')){ u.rate=1.1; u.pitch=1.2; }
    else if(paneId.includes('quant')){ u.rate=0.9; u.pitch=0.7; }
    else { u.rate=1.0; u.pitch=1.0; }
    btn.classList.add('playing');btn.textContent='PLAYING';
    u.onend=()=>{btn.classList.remove('playing');btn.textContent='LISTEN'};
    speechSynthesis.cancel();speechSynthesis.speak(u);
}
'''
    html = html[:start_idx] + correct_audio_js + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Rewrote index.html with perfect font sizing, contrast colors, and fully fixed UI features.")
