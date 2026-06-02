import re

def build_spa_from_backup():
    """
    Takes the PERFECT, uncorrupted index.backup.html and adds ONLY:
    1. SPA tab navigation (Intel, Ledger, Vitals, Alpha)
    2. Mobile dock
    3. Wraps content sections into SPA views
    
    Does NOT touch the CSS, the JS logic, or the component structure.
    """
    with open('public/index.backup.html', 'r', encoding='utf-8') as f:
        original = f.read()

    # ── STEP 1: Extract the original <style> block ──
    style_match = re.search(r'(<style>.*?</style>)', original, re.DOTALL)
    original_style = style_match.group(1)

    # ── STEP 2: Add SPA CSS to the end of the style block ──
    spa_css = """
    /* ═══════════════════════════════════════════
       SPA ROUTER — ADDED ON TOP OF ORIGINAL CSS
       ═══════════════════════════════════════════ */
    .spa-view { display: none; }
    .spa-view.active { display: block; }
    
    /* Sticky header with nav */
    .sticky-hdr { position: sticky; top: 0; z-index: 200; background: rgba(8,8,12,0.92); backdrop-filter: blur(14px); border-bottom: 1px solid var(--dim); display: flex; align-items: center; justify-content: space-between; padding: 10px 24px; }
    .sticky-brand { font-family: var(--font-big); font-size: 1.8rem; letter-spacing: 4px; color: var(--ink); text-decoration: none; line-height: 1; }
    .sticky-brand em { color: var(--red); font-style: normal; }
    .sticky-center { display: flex; align-items: center; gap: 10px; }
    .desktop-nav { display: flex; gap: 18px; align-items: center; }
    .desktop-nav a { font-family: var(--font-mono); font-size: .52rem; color: var(--muted); text-decoration: none; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; transition: color 0.2s; padding-bottom: 4px; border-bottom: 2px solid transparent; }
    .desktop-nav a:hover { color: var(--ink); }
    .desktop-nav a.active { color: var(--red); border-bottom-color: var(--red); }
    
    /* Mobile dock */
    .mobile-dock { display: none; position: fixed; bottom: 0; left: 0; right: 0; background: rgba(8,8,12,0.95); backdrop-filter: blur(12px); border-top: 1px solid var(--dim); z-index: 200; }
    .dock-grid { display: grid; grid-template-columns: repeat(4, 1fr); height: 56px; }
    .dock-btn { display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; border-right: 1px solid var(--s3); transition: background 0.2s; }
    .dock-btn:last-child { border-right: none; }
    .dock-btn:hover { background: rgba(255,255,255,0.03); }
    .dock-icon { font-size: 1.1rem; margin-bottom: 2px; }
    .dock-label { font-family: var(--font-mono); font-size: .42rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }
    .dock-btn.active .dock-label { color: var(--red); }
    
    @media (max-width: 700px) {
      .mobile-dock { display: block; }
      .desktop-nav { display: none; }
      body { padding-bottom: 70px; }
    }
    
    /* Alpha lock page */
    .alpha-lock { max-width: 480px; margin: 100px auto; text-align: center; padding: 48px 32px; background: linear-gradient(135deg, rgba(245,166,35,0.04), var(--s1) 70%); border: 1px solid rgba(245,166,35,0.2); border-radius: 12px; }
    .alpha-lock h2 { font-family: var(--font-ui); font-size: 1.3rem; font-weight: 700; letter-spacing: 1px; color: var(--ink); margin: 16px 0 8px; }
    .alpha-lock p { font-family: var(--font-mono); font-size: .55rem; color: var(--muted); line-height: 1.7; letter-spacing: 0.5px; margin-bottom: 24px; }
    .alpha-btn { display: inline-block; background: var(--gold); color: #000; padding: 12px 28px; font-family: var(--font-mono); font-size: .55rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; border: none; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 20px rgba(245,166,35,0.25); transition: all 0.2s; }
    .alpha-btn:hover { box-shadow: 0 6px 35px rgba(245,166,35,0.4); transform: translateY(-2px); }
    
    /* Page titles for sub-pages */
    .page-title { font-family: var(--font-big); font-size: clamp(2rem, 6vw, 3rem); letter-spacing: 2px; color: var(--ink); margin-bottom: 8px; }
    .page-sub { font-family: var(--font-mono); font-size: .55rem; color: var(--muted); letter-spacing: 1px; margin-bottom: 24px; }
    """
    
    new_style = original_style.replace('</style>', spa_css + '\n  </style>')

    # ── STEP 3: Build the SPA HTML ──
    # Extract original <script> block
    script_match = re.search(r'(<script>.*?</script>)', original, re.DOTALL)
    original_script_content = script_match.group(1) if script_match else '<script></script>'
    
    # We need to get the inner script content to modify the JS
    inner_js = re.search(r'<script>(.*?)</script>', original, re.DOTALL).group(1)

    # Build the complete SPA HTML
    spa_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Chaos Intelligence — ANTICONSENSUS TERMINAL</title>
  <meta name="description" content="Chaos Intelligence live macro war-room brief. AI-powered market intelligence terminal.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400;700&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  {new_style}
</head>
<body>
  <div id="progress"></div>
  <div id="boot"><div class="boot-ey">INITIALIZING WAR ROOM</div><div class="boot-logo">CHAOS<em>.</em></div><div class="boot-bar-w"><div class="boot-bar"></div></div></div>

  <!-- STICKY HEADER WITH SPA NAV -->
  <header class="sticky-hdr">
    <a class="sticky-brand" href="#terminal">CHAOS<em>.</em></a>
    <div class="sticky-center">
      <div class="live-b"><span class="live-d"></span>LIVE BRIEF</div>
    </div>
    <nav class="desktop-nav">
      <a href="#terminal" class="nav-link" data-target="view-terminal">⚡ Intel</a>
      <a href="#ledger" class="nav-link" data-target="view-ledger">📋 Ledger</a>
      <a href="#vitals" class="nav-link" data-target="view-vitals">📊 Vitals</a>
      <a href="#alpha" class="nav-link" data-target="view-alpha" style="color: var(--gold);">🔒 Alpha</a>
    </nav>
  </header>

  <!-- TICKER (original) -->
  <div class="ticker"><div class="tk-lbl"><span class="tk-dot"></span>LIVE</div><div class="tk-scroll"><div class="tk-inner" id="ticker-inner"></div></div></div>

  <!-- ═══════════════════════════════════════════
       VIEW 1: INTEL (main terminal — all original components)
       ═══════════════════════════════════════════ -->
  <div id="view-terminal" class="spa-view active">
    <div class="wrap">
      <header class="hdr">
        <div class="hdr-top"><div class="brand">CHAOS<em>.</em></div><div class="live-b"><span class="live-d"></span>LIVE BRIEF</div></div>
        <div class="dateline"><span id="date-line">LOADING</span><span class="ed-badge" id="session-badge">DAILY BRIEF</span></div>
        <div id="world-clock-bar" class="world-clock-bar"></div>
      </header>
      <div class="hash-badge rv"><span>VERIFIED</span><span class="hash-val" id="hash-val">Hash pending...</span></div>
    </div>

    <div class="wrap"><div class="vitals" id="vitals"></div></div>

    <main class="wrap"><div class="main">
      <article>
        <div class="ed-tag" id="brief-tag">TODAY'S BRIEFING</div>
        <h1 class="hl" id="headline">Loading Chaos Brief</h1>
        <div class="sig-row" id="sig-row"></div>
        <div class="upd"><span class="bull">●</span><span id="updated-line">Loading live data</span></div>

        <section class="rv">
          <div class="sec-title">MARKET FEAR GAUGE</div>
          <div class="gauge-wrap"><div class="gauge-container">
            <svg viewBox="0 0 200 110"><path class="gauge-bg" d="M20,100 A80,80 0 0,1 180,100"/><path class="gauge-fill" id="gauge-arc" d="M20,100 A80,80 0 0,1 180,100" stroke="var(--gold)" stroke-dasharray="251" stroke-dashoffset="251"/></svg>
            <div class="gauge-glow" id="gauge-glow"></div>
            <div class="gauge-val" id="gauge-num">0</div>
            <div class="gauge-label" id="gauge-label">NEUTRAL</div>
          </div></div>
        </section>

        <section class="cx-section rv">
          <div class="sec-title">INTELLIGENCE LEVEL - PICK YOURS</div>
          <div class="cx-tabs" role="tablist">
            <button class="cx-btn" onclick="setCx('eli5',this)"><span class="cx-n">ELI5</span><span class="cx-sub">Simple - 3 min</span></button>
            <button class="cx-btn active" onclick="setCx('analyst',this)"><span class="cx-n">Analyst</span><span class="cx-sub">Intermediate - 5 min</span></button>
            <button class="cx-btn" onclick="setCx('quant',this)"><span class="cx-n">Quant</span><span class="cx-sub">Advanced - 7 min</span></button>
          </div>
          <div class="pane" id="pane-eli5"></div>
          <div class="pane active" id="pane-analyst"></div>
          <div class="pane" id="pane-quant"></div>
        </section>
      </article>

      <section class="forces rv"><div class="sec-title">ACTIVE MACRO FORCES</div><div class="forces-grid" id="forces-grid"></div></section>
      <section class="glass-card rv" style="margin-bottom:24px" id="agent-consensus"></section>
      <section class="chaos rv" id="chaos-line-card"></section>
      
      <section class="rv"><div class="sec-title">THE PLAYS - 3 WAYS TO TRADE THIS</div><div class="plays-grid" id="plays-grid"></div><div style="font-family:var(--font-mono);font-size:.44rem;color:var(--muted);margin-top:10px;letter-spacing:.5px">THESIS ONLY - NOT FINANCIAL ADVICE</div></section>
      
      <section class="trap rv" id="trap-card"></section>
      <section class="edge-section rv" id="edge-card"></section>
    </div></main>
  </div>

  <!-- ═══════════════════════════════════════════
       VIEW 2: LEDGER
       ═══════════════════════════════════════════ -->
  <div id="view-ledger" class="spa-view">
    <div class="wrap" style="padding-top:40px">
      <div class="page-title">PUBLIC SIGNAL LEDGER</div>
      <div class="page-sub">FULL SIGNAL HISTORY WITH RESOLUTION STATUS</div>
      <section class="glass-card rv vis" style="margin-bottom:48px"><div class="sec-title">SIGNAL LEDGER</div><div id="ledger"></div></section>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       VIEW 3: VITALS
       ═══════════════════════════════════════════ -->
  <div id="view-vitals" class="spa-view">
    <div class="wrap" style="padding-top:40px">
      <div class="page-title">MACRO DASHBOARD</div>
      <div class="page-sub">CROSS-MARKET INTELLIGENCE</div>
      <section class="glass-card macro rv vis"><div class="sec-title">MACRO DASHBOARD</div><div class="mgrid" id="macro-grid"></div></section>
      <section class="ctx rv vis"><div class="sec-title">CROSS-MARKET CONTEXT</div><div class="ctx-grid" id="context-grid"></div></section>
      <section class="poly rv vis" id="poly-card"></section>
      <section class="wires rv vis"><div class="wires-h"><span>INTEL WIRES</span><span style="font-size:.42rem;opacity:.5">CLICK TO EXPAND</span></div><div id="wires"></div></section>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════
       VIEW 4: ALPHA (locked)
       ═══════════════════════════════════════════ -->
  <div id="view-alpha" class="spa-view">
    <div class="wrap">
      <div class="alpha-lock">
        <div style="font-size:3rem;margin-bottom:16px">🔒</div>
        <h2>Unlock Whale Orderbook Telemetry</h2>
        <p>Get real-time execution parameters and webhook trade updates pushed direct to your console interface. Unfiltered algorithmic dissent straight from the pool trackers.</p>
        <button class="alpha-btn">UNLOCK ACCESS TIER</button>
      </div>
    </div>
  </div>

  <!-- MOBILE DOCK -->
  <div class="mobile-dock">
    <div class="dock-grid">
      <a href="#terminal" class="dock-btn nav-link" data-target="view-terminal"><span class="dock-icon">⚡</span><span class="dock-label">INTEL</span></a>
      <a href="#ledger" class="dock-btn nav-link" data-target="view-ledger"><span class="dock-icon">📋</span><span class="dock-label">LEDGER</span></a>
      <a href="#vitals" class="dock-btn nav-link" data-target="view-vitals"><span class="dock-icon">📊</span><span class="dock-label">VITALS</span></a>
      <a href="#alpha" class="dock-btn nav-link" data-target="view-alpha"><span class="dock-icon">🔒</span><span class="dock-label" style="color:var(--gold)">ALPHA</span></a>
    </div>
  </div>

  <footer class="wrap"><div class="ftr"><div class="ftr-brand">CHAOS<em>.</em></div><div class="ftr-disc">Not financial advice. AI-generated from public data. Public ledger required before performance claims. Chaos Intelligence.</div></div></footer>

  <script>
    // ═══════════════════════════════════════════
    // SPA ROUTER (new)
    // ═══════════════════════════════════════════
    function runClientRouter() {{
      const hash = window.location.hash || '#terminal';
      const targets = {{ '#terminal': 'view-terminal', '#ledger': 'view-ledger', '#vitals': 'view-vitals', '#alpha': 'view-alpha' }};
      const viewId = targets[hash] || 'view-terminal';
      document.querySelectorAll('.spa-view').forEach(v => v.classList.remove('active'));
      const el = document.getElementById(viewId);
      if (el) el.classList.add('active');
      document.querySelectorAll('.nav-link').forEach(link => {{
        link.classList.toggle('active', link.getAttribute('data-target') === viewId);
      }});
      window.scrollTo(0, 0);
    }}
    window.addEventListener('hashchange', runClientRouter);
    window.addEventListener('load', runClientRouter);

    // ═══════════════════════════════════════════
    // ORIGINAL JS (untouched from index.backup.html)
    // ═══════════════════════════════════════════
{inner_js}
  </script>
</body>
</html>"""

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(spa_html)
    
    print("SUCCESS: Built SPA from uncorrupted index.backup.html")
    print(f"  Original backup: 295 lines, 41993 bytes")
    print(f"  New SPA output:  {len(spa_html)} bytes")

build_spa_from_backup()
