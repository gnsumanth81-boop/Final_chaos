import re

def rebuild_vanilla_css():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    new_css = """
    /* ═══════════════════════════════════════════
       RESTORED VANILLA CSS MASTERPIECE
       ═══════════════════════════════════════════ */
    :root {
      --bg: #08080c;
      --bg2: #121218;
      --panel: #16161e;
      --panel-hover: #1c1c26;
      --s3: #22222e;
      
      --ink: #ffffff;
      --muted: #8b8b9e;
      
      --red: #ff3355;
      --red-dim: rgba(255, 51, 85, 0.1);
      
      --green: #00ff66;
      --green-dim: rgba(0, 255, 102, 0.1);
      
      --gold: #ffaa00;
      --gold-dim: rgba(255, 170, 0, 0.1);
      
      --blue: #4cc9f0;
      --purple: #9d6cf8;
      
      --font-body: 'Crimson Pro', Georgia, serif;
      --font-mono: 'Space Mono', 'JetBrains Mono', monospace;
      --font-sans: 'Inter', sans-serif;
    }
    
    body {
      background-color: var(--bg);
      color: var(--ink);
      font-family: var(--font-body);
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }
    
    /* SPA Additions */
    .spa-view { display: none; }
    .spa-view.active { display: block; }
    
    /* Layout */
    .wrap { max-width: 800px; margin: 0 auto; padding: 20px; }
    
    /* Typography */
    h1, h2, h3, h4 { font-family: var(--font-sans); margin: 0; }
    .sec-title {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--ink);
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 20px;
    }
    
    /* Global Helpers */
    .bull { color: var(--green); }
    .bear { color: var(--red); }
    .neut { color: var(--gold); }
    .volt { color: var(--gold); }
    
    /* Vitals */
    .vitals { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--s3); border-bottom: 1px solid var(--s3); }
    .vital { background: var(--bg2); padding: 20px; text-align: center; }
    .vital-val { font-family: var(--font-sans); font-size: 2rem; font-weight: 700; line-height: 1.2; }
    .vital-lbl { font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); text-transform: uppercase; margin-top: 5px; }
    .vital-sub { font-family: var(--font-mono); font-size: 0.55rem; color: var(--muted); margin-top: 5px; }
    
    /* Gauge */
    .gauge-section { text-align: center; margin: 40px 0; }
    .gauge-container { position: relative; width: 250px; height: 140px; margin: 0 auto; overflow: hidden; }
    .gauge-bg { fill: none; stroke: var(--s3); stroke-width: 12; }
    .gauge-fill { fill: none; stroke-width: 12; stroke-linecap: round; transition: stroke-dashoffset 1s ease-out; }
    .gauge-val { position: absolute; bottom: 10px; left: 0; right: 0; font-family: var(--font-sans); font-size: 3.5rem; font-weight: 800; line-height: 1; }
    .gauge-label { position: absolute; bottom: 0; left: 0; right: 0; font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; color: var(--muted); letter-spacing: 2px; }
    
    /* Chaos Line & Intro */
    .chaos-block {
      border-left: 3px solid var(--gold);
      background: rgba(255, 170, 0, 0.05);
      padding: 20px 25px;
      margin: 40px 0;
      position: relative;
    }
    .chaos-lbl {
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--gold);
      text-transform: uppercase;
      letter-spacing: 3px;
      margin-bottom: 15px;
      display: block;
    }
    .chaos-text {
      font-family: var(--font-body);
      font-size: 1.35rem;
      font-style: italic;
      color: var(--ink);
      line-height: 1.5;
      margin-bottom: 20px;
    }
    .share-row { display: flex; gap: 10px; }
    .btn {
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      border: none;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .btn-red { background: var(--red); color: white; }
    .btn-dark { background: var(--panel); color: white; border: 1px solid var(--s3); }
    .btn-outline-gold { background: transparent; color: var(--gold); border: 1px solid var(--gold); }
    
    /* Intelligence Tabs */
    .cx-tabs { display: grid; grid-template-columns: repeat(3, 1fr); background: var(--bg2); border-bottom: 2px solid var(--s3); }
    .cx-btn {
      background: transparent; border: none; padding: 20px 10px; color: var(--muted);
      cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center;
      transition: all 0.2s; border-bottom: 2px solid transparent; margin-bottom: -2px;
    }
    .cx-btn.active { color: var(--ink); border-bottom: 2px solid var(--red); background: linear-gradient(to top, rgba(255,51,85,0.1), transparent); }
    .cx-n { font-family: var(--font-sans); font-size: 1.2rem; font-weight: 800; margin-bottom: 5px; }
    .cx-sub { font-family: var(--font-mono); font-size: 0.65rem; }
    .pane { display: none; padding: 30px 0; }
    .pane.active { display: block; }
    .pane p { font-size: 1.15rem; color: var(--ink); }
    .pane-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .pane-title { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; }
    
    /* Agent Consensus */
    .agent-panel {
      display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px;
    }
    .agent-box {
      background: var(--bg2);
      border: 1px solid var(--s3);
      border-radius: 8px;
      padding: 20px;
      text-align: center;
    }
    .ag-n { font-family: var(--font-mono); font-size: 0.75rem; color: var(--ink); font-weight: 700; letter-spacing: 1px; margin-bottom: 10px; }
    .ag-bias { font-family: var(--font-mono); font-size: 0.9rem; font-weight: 700; margin-bottom: 15px; }
    .ag-t { font-family: var(--font-body); font-size: 1.05rem; color: var(--muted); line-height: 1.5; }
    .debate-pill {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--gold);
      border: 1px solid var(--gold);
      border-radius: 20px;
      padding: 6px 16px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin: 0 auto;
    }
    
    /* Macro Forces */
    .ctx-grid { display: grid; gap: 10px; }
    .ctx-box {
      padding: 12px; text-align: center; border-radius: 6px;
      font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700;
      border: 1px solid var(--s3); background: var(--bg2); color: var(--muted);
      transition: all 0.3s;
    }
    .ctx-box.active { border-color: var(--red); color: var(--red); background: var(--red-dim); box-shadow: 0 0 15px var(--red-dim); }
    
    /* Macro Dashboard */
    .dashboard-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 40px; }
    .dash-box { background: var(--bg2); border-radius: 8px; padding: 15px; border: 1px solid var(--s3); }
    .dash-lbl { font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
    .dash-val { font-family: var(--font-sans); font-size: 1.5rem; font-weight: 800; line-height: 1; margin-bottom: 5px; }
    .dash-sub { font-family: var(--font-mono); font-size: 0.65rem; color: var(--muted); }
    
    /* Trap / Edge */
    .trap-edge { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 40px 0; }
    .te-box { background: var(--bg2); border-radius: 8px; padding: 20px; border: 1px solid; }
    .te-trap { border-color: rgba(255, 51, 85, 0.3); }
    .te-edge { border-color: rgba(157, 108, 248, 0.3); }
    .te-title { font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    .te-trap .te-title { color: var(--red); }
    .te-edge .te-title { color: var(--purple); }
    .te-desc { font-family: var(--font-body); font-size: 1.1rem; color: var(--ink); line-height: 1.5; }
    
    /* Header & Navigation */
    .sticky-hdr { position: sticky; top: 0; background: rgba(8,8,12,0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--s3); z-index: 100; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
    .brand { font-family: var(--font-sans); font-size: 1.2rem; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
    .brand em { color: var(--red); font-style: normal; }
    .desktop-nav { display: flex; gap: 20px; }
    .desktop-nav a { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); text-decoration: none; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; transition: color 0.2s; }
    .desktop-nav a:hover { color: white; }
    .desktop-nav a.active { color: var(--gold); border-bottom: 2px solid var(--gold); padding-bottom: 4px; }
    
    /* Polymarket */
    .poly-card { background: var(--bg2); border: 1px solid var(--s3); border-radius: 8px; padding: 20px; }
    .poly-tag { font-family: var(--font-mono); font-size: 0.65rem; color: var(--blue); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; display: block; }
    .poly-q { font-family: var(--font-sans); font-size: 1.2rem; font-weight: 700; margin-bottom: 15px; }
    .poly-row { display: flex; align-items: center; gap: 15px; }
    .poly-odds { font-family: var(--font-sans); font-size: 1.5rem; font-weight: 800; color: var(--ink); width: 60px; }
    .poly-track { flex: 1; height: 6px; background: var(--s3); border-radius: 3px; overflow: hidden; }
    .poly-fill { height: 100%; background: var(--blue); border-radius: 3px; transition: width 0.5s ease-out; }
    """
    
    # We will replace the <style> block in index.html with our new one
    html = re.sub(r'<style>.*?</style>', f'<style>\n{new_css}\n</style>', html, flags=re.DOTALL)
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Injected perfect handcrafted Vanilla CSS.")

rebuild_vanilla_css()
