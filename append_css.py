import re

def append_css():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    extra_css = """
    /* ═══════════════════════════════════════════
       ADDITIONAL VANILLA COMPONENTS
       ═══════════════════════════════════════════ */
       
    /* Ticker */
    .ticker { display: flex; align-items: center; background: var(--bg2); border-bottom: 1px solid var(--s3); padding: 5px 0; font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); }
    .tk-lbl { padding: 0 15px; border-right: 1px solid var(--s3); display: flex; align-items: center; gap: 6px; font-weight: 700; }
    .tk-dot { width: 6px; height: 6px; background: var(--red); border-radius: 50%; box-shadow: 0 0 10px var(--red); }
    .tk-scroll { overflow: hidden; white-space: nowrap; flex: 1; padding: 0 15px; }
    .tk-inner { animation: scroll 20s linear infinite; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Pills & Tags */
    .live-pill { display: inline-flex; align-items: center; gap: 6px; font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; color: var(--red); border: 1px solid var(--red-dim); padding: 4px 10px; border-radius: 4px; background: rgba(255,51,85,0.05); }
    .live-dot { width: 6px; height: 6px; background: var(--red); border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .sig-pill { display: inline-block; font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-left: 10px; }
    .sig-pill.bull { background: var(--green-dim); color: var(--green); border: 1px solid rgba(0,255,102,0.3); }
    .sig-pill.bear { background: var(--red-dim); color: var(--red); border: 1px solid rgba(255,51,85,0.3); }
    .sig-pill.neut { background: var(--gold-dim); color: var(--gold); border: 1px solid rgba(255,170,0,0.3); }
    .sig-pill.volt { background: var(--gold-dim); color: var(--gold); border: 1px solid rgba(255,170,0,0.3); }
    
    /* Headlines & Briefing */
    .ed-tag { font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; display: block; }
    h1.hl { font-size: 2.5rem; line-height: 1.1; margin-bottom: 20px; font-weight: 800; color: white; }
    .sig-row { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }
    .sig { font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; background: var(--s3); }
    .ts-badge, .regime-tag, .conf { font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; background: var(--bg2); border: 1px solid var(--s3); color: var(--muted); }
    .upd { font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); display: flex; align-items: center; gap: 6px; }
    .upd .bull { color: var(--green); }
    
    /* 3 Plays (Actionable Bets) */
    .plays-grid { display: grid; gap: 15px; margin-top: 20px; }
    .play-card { background: var(--bg2); border: 1px solid var(--s3); border-radius: 8px; padding: 20px; border-left: 4px solid var(--muted); transition: transform 0.2s; }
    .play-card:hover { transform: translateX(5px); }
    .play-card:has(.bull) { border-left-color: var(--green); }
    .play-card:has(.bear) { border-left-color: var(--red); }
    .play-card:has(.neut) { border-left-color: var(--gold); }
    .play-tag { font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; margin-bottom: 10px; display: inline-block; }
    .play-th { font-family: var(--font-sans); font-size: 1.1rem; font-weight: 700; margin-bottom: 10px; color: white; }
    .play-det { font-family: var(--font-body); font-size: 1rem; color: var(--muted); line-height: 1.5; }
    .free-badge { color: var(--gold); font-size: 0.65rem; }
    
    /* Glass Cards */
    .glass-card { background: rgba(18,18,24,0.6); backdrop-filter: blur(10px); border: 1px solid var(--s3); border-radius: 12px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .page-title { font-family: var(--font-sans); font-size: 2rem; font-weight: 800; color: white; margin-bottom: 10px; }
    
    /* Ledger */
    .track-section { margin-top: 20px; }
    .track-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid var(--s3); padding-bottom: 10px; }
    .track-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .track-row:last-child { border-bottom: none; }
    .track-date { font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); width: 80px; }
    .track-hl { font-family: var(--font-sans); font-size: 0.9rem; font-weight: 600; color: white; flex: 1; padding: 0 15px; }
    .track-result { font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700; text-transform: uppercase; text-align: right; }
    .track-result.open { color: var(--gold); }
    .track-result.bull { color: var(--green); }
    .track-result.bear { color: var(--red); }
    
    /* General spacing */
    .wrap > section { margin-bottom: 50px; }
    """
    
    html = html.replace('</style>', extra_css + '\n</style>')
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Injected additional Vanilla components CSS.")

append_css()
