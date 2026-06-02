import re

def rebuild_spa():
    with open('reconstructed.html', 'r', encoding='utf-8') as f:
        old_html = f.read()

    style_match = re.search(r'<style>(.*?)</style>', old_html, re.DOTALL)
    styles = style_match.group(1) if style_match else ""

    new_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CHAOS // ANTICONSENSUS TERMINAL</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
/*STYLES_PLACEHOLDER*/
    /* SPA Additions */
    .spa-view { display: none; }
    .spa-view.active { display: block; }
    .desktop-nav { display: flex; gap: 20px; }
    .desktop-nav a { color: var(--muted); text-decoration: none; font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; transition: color 0.2s; cursor: pointer; }
    .desktop-nav a:hover { color: #fff; }
    .desktop-nav a.active { color: var(--red); border-bottom: 2px solid var(--red); padding-bottom: 4px; }
    
    .mobile-dock { display: none; position: fixed; bottom: 0; left: 0; right: 0; background: rgba(7,8,10,0.95); backdrop-filter: blur(10px); border-top: 1px solid var(--s3); z-index: 100; }
    .dock-grid { display: grid; grid-template-columns: repeat(4, 1fr); height: 60px; }
    .dock-btn { display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; border-right: 1px solid var(--s3); }
    .dock-btn:last-child { border-right: none; }
    .dock-icon { font-size: 1.2rem; margin-bottom: 2px; }
    .dock-label { font-family: var(--font-mono); font-size: 0.5rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
    .dock-btn.active .dock-label { color: var(--red); }
    
    @media (max-width: 768px) {
      .mobile-dock { display: block; }
      .desktop-nav { display: none; }
      body { padding-bottom: 80px; }
    }
    
    .alpha-lock { max-width: 500px; margin: 100px auto; text-align: center; background: var(--bg2); border: 1px solid var(--orange); padding: 40px; box-shadow: 0 0 30px rgba(255, 170, 0, 0.1); }
    .alpha-lock h2 { font-family: var(--font-body); font-size: 1.5rem; color: #fff; margin: 15px 0; }
    .alpha-lock p { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); line-height: 1.6; margin-bottom: 24px; }
    .alpha-btn { background: var(--orange); color: #000; padding: 12px 24px; font-family: var(--font-mono); font-weight: 700; text-transform: uppercase; border: none; cursor: pointer; width: 100%; transition: opacity 0.2s; }
    .alpha-btn:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <!-- HEADER -->
  <header class="sticky-hdr">
    <div class="sticky-inner">
      <a class="sticky-brand" href="#terminal">CHAOS<em>.</em></a>
      <div class="sticky-center" style="margin-left: 20px;">
        <span class="live-pill"><span class="live-dot"></span>LIVE</span>
        <span class="sig-pill neut" id="hdr-signal">—</span>
      </div>
      <nav class="desktop-nav" style="margin-left: auto;">
        <a href="#terminal" class="nav-link" data-target="view-terminal">⚡ Intel</a>
        <a href="#ledger" class="nav-link" data-target="view-ledger">📋 Ledger</a>
        <a href="#vitals" class="nav-link" data-target="view-vitals">📊 Vitals</a>
        <a href="#alpha" class="nav-link" data-target="view-alpha" style="color: var(--orange);">🔒 Alpha</a>
      </nav>
    </div>
  </header>

  <!-- TICKER -->
  <div class="ticker"><div class="tk-lbl"><span class="tk-dot"></span>LIVE</div><div class="tk-scroll"><div class="tk-inner" id="ticker-inner"></div></div></div>

  <!-- VIEWS -->
  <main>
    <!-- VIEW: INTEL -->
    <div id="view-terminal" class="spa-view active">
      <div class="wrap"><div class="vitals" id="vitals"></div></div>
      <div class="wrap">
        <section class="gauge-section rv vis">
          <div class="sec-title">MARKET FEAR GAUGE</div>
          <div class="gauge-wrap">
            <div class="gauge-container">
              <svg viewBox="0 0 200 110">
                <path class="gauge-bg" d="M20,100 A80,80 0 0,1 180,100"/>
                <path class="gauge-fill" id="gauge-arc" d="M20,100 A80,80 0 0,1 180,100" stroke="var(--gold)" stroke-dasharray="251" stroke-dashoffset="251"/>
              </svg>
              <div class="gauge-glow" id="gauge-glow"></div>
              <div class="gauge-val" id="gauge-num">0</div>
              <div class="gauge-label" id="gauge-label">LOADING</div>
            </div>
          </div>
        </section>
      </div>

      <div class="wrap">
        <div class="main-section">
          <article class="rv vis">
            <div class="ed-tag" id="brief-tag">TODAY'S BRIEFING</div>
            <h1 class="hl" id="headline">Loading Chaos Brief</h1>
            <div class="sig-row" id="sig-row"></div>
            <div class="upd"><span class="bull">●</span><span id="updated-line">Loading live data</span></div>
          </article>
          
          <section class="brief rv vis">
            <div id="story-intro" style="margin-bottom:24px; font-weight:500">Loading narrative...</div>
            <div class="chaos-text" id="chaos-text">&ldquo;Loading...&rdquo;</div>
            <div class="share-row" id="share-row">
              <button class="s-btn red" onclick="copyLine()">Copy Line</button>
              <button class="voice-btn" onclick="chaosSpeak('chaos-text',this,'chaos')">🔊 LISTEN</button>
            </div>
          </section>

          <!-- Intelligence Tabs -->
          <section class="cx-section rv vis">
            <div class="sec-title">INTELLIGENCE LEVEL — PICK YOURS</div>
            <div class="cx-tabs" role="tablist">
              <button class="cx-btn active" onclick="setCx('eli5',this)"><span class="cx-emoji">🧠</span><span class="cx-n">ELI5</span><span class="cx-sub">Simple · 3 min</span></button>
              <button class="cx-btn" onclick="setCx('analyst',this)"><span class="cx-emoji">📊</span><span class="cx-n">Analyst</span><span class="cx-sub">Intermediate · 5 min</span></button>
              <button class="cx-btn" onclick="setCx('quant',this)"><span class="cx-emoji">🔬</span><span class="cx-n">Quant</span><span class="cx-sub">Advanced · 7 min</span></button>
            </div>
            <div class="pane active" id="pane-eli5">
              <div class="flex" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div class="sec-title" style="margin:0;">ELI5 - SIMPLE</div>
                <button class="voice-btn" onclick="chaosSpeak('text-eli5',this,'eli5')">🔊 LISTEN</button>
              </div>
              <p id="text-eli5">Loading...</p>
            </div>
            <div class="pane" id="pane-analyst">
              <div class="flex" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div class="sec-title" style="margin:0;">ANALYST - INTERMEDIATE</div>
                <button class="voice-btn" onclick="chaosSpeak('text-analyst',this,'analyst')">🔊 LISTEN</button>
              </div>
              <p id="text-analyst">Loading...</p>
            </div>
            <div class="pane" id="pane-quant">
              <div class="flex" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <div class="sec-title" style="margin:0;">QUANT - ADVANCED</div>
                <button class="voice-btn" onclick="chaosSpeak('text-quant',this,'quant')">🔊 LISTEN</button>
              </div>
              <p id="text-quant">Loading...</p>
            </div>
          </section>
          
          <!-- MACRO FORCES -->
          <section class="rv vis">
            <div class="sec-title">ACTIVE MACRO FORCES</div>
            <div class="ctx-grid" id="macro-forces-grid" style="grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 24px;">
              <!-- Injected by JS -->
            </div>
          </section>

          <!-- Agent Consensus -->
          <section class="glass-card rv vis" style="margin-bottom:48px" id="agent-consensus">
            <div class="sec-title">AGENT CONSENSUS</div>
            <div class="agent-panel" id="agent-panel-grid">
              <!-- Injected by JS -->
            </div>
            <div class="debate-row" id="debate-row" style="text-align:center; padding: 16px; border-top: 1px solid var(--s3); font-family: var(--font-mono); font-size: 0.6rem; color: var(--muted); margin-top: 16px;">
              DEBATE RESOLVED
            </div>
          </section>

          <!-- 3 Plays -->
          <section class="plays-section rv vis">
            <div class="sec-title">THE ANTICIPATED BETS <span class="free-badge">// OVERRIDING THE MACHINE</span></div>
            <div class="plays-grid" id="plays-grid"></div>
          </section>
          
          <section class="trap-edge rv vis" style="margin-bottom:48px;">
            <div class="trap-box"><div class="te-title">⚠️ MARKET TRAP</div><div class="te-desc" id="trap-text">Loading...</div></div>
            <div class="edge-box"><div class="te-title">💎 THE EDGE</div><div class="te-desc" id="edge-text">Loading...</div></div>
          </section>
        </div>
      </div>
    </div>

    <!-- VIEW: LEDGER -->
    <div id="view-ledger" class="spa-view">
      <div class="wrap" style="padding-top: 40px;">
        <div class="page-title">PUBLIC SIGNAL LEDGER</div>
        <p style="font-family:var(--font-mono);font-size:1.07rem;color:var(--muted);margin-bottom:20px">Full signal history with resolution status.</p>
        <div class="track-section">
          <div class="glass-card">
            <div class="track-header"><div class="sec-title" style="margin-bottom:0">SIGNAL LEDGER</div><div class="win-rate" id="win-rate" style="display:none"></div></div>
            <div id="track-body"></div>
            <div class="verify-link"><a href="#" target="_blank">Verify Ledger Authenticity ↗</a></div>
          </div>
        </div>
      </div>
    </div>

    <!-- VIEW: VITALS -->
    <div id="view-vitals" class="spa-view">
      <div class="wrap" style="padding-top: 40px;">
        <div class="page-title">MACRO DASHBOARD</div>
        <div class="ctx-grid" id="context-grid" style="margin-bottom: 40px;"></div>
        
        <div class="sec-title">TOP PREDICTION MARKET</div>
        <div class="glass-card" id="poly-card" style="margin-bottom: 40px;"></div>
        
        <div class="sec-title">INTEL WIRES</div>
        <div class="glass-card" id="wires-section">
          <div id="wires-list" style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); line-height: 1.6; max-height: 200px; overflow-y: auto;"></div>
        </div>
      </div>
    </div>

    <!-- VIEW: ALPHA -->
    <div id="view-alpha" class="spa-view">
      <div class="wrap">
        <div class="alpha-lock">
          <div style="font-size: 3rem; margin-bottom: 20px;">🔒</div>
          <h2>Unlock Whale Orderbook Telemetry</h2>
          <p>Get real-time execution parameters and webhook trade updates pushed direct to your console interface. Unfiltered algorithmic dissent straight from the pool trackers.</p>
          <button class="alpha-btn">UNLOCK ACCESS TIER</button>
        </div>
      </div>
    </div>
  </main>

  <!-- MOBILE DOCK -->
  <div class="mobile-dock">
    <div class="dock-grid">
      <a href="#terminal" class="dock-btn nav-link" data-target="view-terminal">
        <span class="dock-icon">⚡</span>
        <span class="dock-label">INTEL</span>
      </a>
      <a href="#ledger" class="dock-btn nav-link" data-target="view-ledger">
        <span class="dock-icon">📋</span>
        <span class="dock-label">LEDGER</span>
      </a>
      <a href="#vitals" class="dock-btn nav-link" data-target="view-vitals">
        <span class="dock-icon">📊</span>
        <span class="dock-label">VITALS</span>
      </a>
      <a href="#alpha" class="dock-btn nav-link" data-target="view-alpha">
        <span class="dock-icon">🔒</span>
        <span class="dock-label" style="color: var(--orange);">ALPHA</span>
      </a>
    </div>
  </div>

  <script>
    // SPA ROUTER
    function runClientRouter() {
      const hash = window.location.hash || '#terminal';
      const targets = { '#terminal': 'view-terminal', '#ledger': 'view-ledger', '#vitals': 'view-vitals', '#alpha': 'view-alpha' };
      const selectedViewId = targets[hash] || 'view-terminal';
      
      document.querySelectorAll('.spa-view').forEach(view => view.classList.remove('active'));
      const activeSection = document.getElementById(selectedViewId);
      if(activeSection) activeSection.classList.add('active');

      document.querySelectorAll('.nav-link').forEach(link => {
        if(link.getAttribute('data-target') === selectedViewId) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
      window.scrollTo(0,0);
    }
    window.addEventListener('hashchange', runClientRouter);
    window.addEventListener('load', runClientRouter);

    // UTILITIES
    let currentLine = "";
    function num(v, d=0){const p=parseFloat(v);return isNaN(p)?d:p}
    function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
    function animateGauge(t){const a=document.getElementById('gauge-arc'),n=document.getElementById('gauge-num');a.style.strokeDashoffset=251-(t/100)*251;let c=0;const s=Math.max(1,Math.round(t/36));const iv=setInterval(()=>{c+=s;if(c>=t){c=t;clearInterval(iv)}n.textContent=c},25)}
    function setCx(cx,btn){if(window.speechSynthesis)speechSynthesis.cancel();document.querySelectorAll('.voice-btn').forEach(b=>{b.classList.remove('playing');b.textContent='🔊 LISTEN'});document.querySelectorAll('.cx-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));btn.classList.add('active');document.getElementById('pane-'+cx).classList.add('active')}
    function copyLine(){navigator.clipboard?.writeText(`"${currentLine}" — Chaos Intelligence`); alert("Copied!");}
    
    // VOICE
    function findVoice(patterns) {
      const vs = speechSynthesis.getVoices();
      for (const p of patterns) {
        const v = vs.find(x => p.test(x.name));
        if (v) return v;
      }
      return vs.find(x => /en-(US|GB)/i.test(x.lang)) || vs[0];
    }
    function chaosSpeak(id, btn, type) {
      if (!window.speechSynthesis) return alert('Speech synthesis not supported.');
      const el = document.getElementById(id);
      if (!el) return;
      let text = el.innerText;
      if (btn.classList.contains('playing')) {
        speechSynthesis.cancel();
        btn.classList.remove('playing');
        btn.innerHTML = '🔊 LISTEN';
        return;
      }
      document.querySelectorAll('.voice-btn').forEach(b => { b.classList.remove('playing'); b.innerHTML = '🔊 LISTEN'; });
      speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      switch(type) {
        case 'eli5': u.rate=1.0; u.pitch=1.2; u.voice=findVoice([/Samantha/i, /Google US/i]); break;
        case 'analyst': u.rate=1.1; u.pitch=1.0; u.voice=findVoice([/Daniel/i, /Google UK/i]); break;
        case 'quant': u.rate=1.25; u.pitch=0.9; u.voice=findVoice([/Fred/i, /Microsoft Mark/i]); break;
        default: u.rate=0.85; u.pitch=0.8; u.voice=findVoice([/Moira/i, /Microsoft Zira/i]);
      }
      btn.classList.add('playing'); btn.innerHTML = '⏹ STOP';
      u.onend = () => { btn.classList.remove('playing'); btn.innerHTML = '🔊 LISTEN'; };
      u.onerror = () => { btn.classList.remove('playing'); btn.innerHTML = '🔊 LISTEN'; };
      speechSynthesis.speak(u);
    }
    if ('speechSynthesis' in window) { speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices(); }

    // RENDER COMPONENTS
    function playCardFree(p){
        const isB=p.type==='AGGRESSIVE'||p.type==='MOMENTUM'||p.type==='HUNT',isC=p.type==='CONTRARIAN'||p.type==='SQUEEZE';
        const cls=isB?'bull':isC?'neut':'';
        return`<div class="play-card"><div class="play-tag ${cls}">${esc(p.type)}</div><div class="play-th">${esc(p.thesis||p.title)}</div><div class="play-det">${esc(p.details||p.description)}</div></div>`;
    }

    // MAIN LOAD
    async function loadTerminalPayload() {
      try {
        const response = await fetch('./api/latest.json', {cache:'no-store'});
        if(!response.ok) throw new Error(`HTTP Outage: ${response.status}`);
        const data = await response.json();
        
        const m = data.market || {};
        const b = data.brief || {};
        
        // Sometimes the data is flat, sometimes nested. Let's support both.
        const signal = b.signal || data.signal || 'NEUTRAL';
        const scls = signal==='BULLISH'?'bull':signal==='BEARISH'?'bear':signal==='VOLATILE'?'volt':'neut';
        const fear = num(m.fearIndex || data.tensionScore, 50);
        const fearCls = fear<=25?'bear':fear>=75?'bull':'neut';
        const fearColor = fear<=25?'#ff003c':fear>=75?'#00ff66':'#ffaa00';
        const btcCls = num(m.btcChange || -1.54)>=0?'bull':'bear';
        currentLine = b.chaos_line || data.metaphor || '';

        // Header
        const hs = document.getElementById('hdr-signal');
        hs.textContent = signal;
        hs.className = `sig-pill ${scls}`;

        // Vitals
        document.getElementById('vitals').innerHTML = [
            `<div class="vital"><div class="vital-val ${btcCls}">${esc(m.btcPrice||'$75,634')}</div><div class="vital-lbl">BTC/USD</div><div class="vital-sub">24h ${num(m.btcChange||-1.54).toFixed(2)}%</div></div>`,
            `<div class="vital"><div class="vital-val ${scls}">${esc(signal)}</div><div class="vital-lbl">Signal</div><div class="vital-sub">AI · ${b.active_regime||'Transition'}</div></div>`,
            `<div class="vital"><div class="vital-val neut">${b.confidence||data.confidenceScore||0}%</div><div class="vital-lbl">Confidence</div><div class="vital-sub">${(b.forces||data.activeForces||[]).length} forces</div></div>`
        ].join('');

        // Gauge
        document.getElementById('gauge-arc').setAttribute('stroke',fearColor);
        document.getElementById('gauge-glow').style.background=fearColor;
        document.getElementById('gauge-num').className=`gauge-val ${fearCls}`;
        document.getElementById('gauge-label').textContent=String(m.fearLabel||'Neutral').toUpperCase();
        setTimeout(()=>animateGauge(fear),200);

        // Headline
        document.getElementById('brief-tag').textContent=`TODAY'S BRIEFING — ${(b.dateline||'GLOBAL').toUpperCase()}`;
        document.getElementById('headline').textContent=b.headline||data.headline||'Market Update';
        document.getElementById('sig-row').innerHTML=`<span class="sig ${scls}">${esc(signal)}</span><span class="ts-badge">${esc(b.time_sensitivity||'THIS WEEK')}</span>${b.active_regime?`<span class="regime-tag">${esc(b.active_regime)}</span>`:''}<span class="conf">${b.confidence||data.confidenceScore||0}% AI CONFIDENCE</span>`;
        document.getElementById('updated-line').textContent=`LIVE DATA · ${m.label||'NYSE CLOSED'}`;

        // Narrative
        document.getElementById('story-intro').textContent = b.eli5 || data.intelligenceLevels?.eli5 || "Markets are nervous.";
        document.getElementById('chaos-text').innerHTML=`&ldquo;${esc(currentLine)}&rdquo;`;

        // Intelligence Tabs
        document.getElementById('text-eli5').innerText = b.eli5 || data.intelligenceLevels?.eli5 || "--";
        document.getElementById('text-analyst').innerText = b.analyst || data.intelligenceLevels?.analyst || "--";
        document.getElementById('text-quant').innerText = b.quant || data.intelligenceLevels?.quant || "--";

        // Macro Forces
        const allForces = ["MONEY", "TECH", "ENERGY", "POLITICS", "WAR", "DEBT", "JOBS", "FOOD", "PEOPLE"];
        const activeForces = b.forces || data.activeForces || ["MONEY"];
        document.getElementById('macro-forces-grid').innerHTML = allForces.map(f => {
            const active = activeForces.includes(f);
            return `<div class="ctx-box" style="padding: 10px; text-align: center; border: 1px solid ${active ? 'var(--red)' : 'var(--s3)'}; background: ${active ? 'rgba(255,0,60,0.05)' : 'transparent'}; color: ${active ? 'var(--red)' : 'var(--muted)'}; opacity: ${active ? '1' : '0.4'}; font-weight: bold; border-radius: 6px; font-size: 0.6rem;">${active ? '• ' : ''}${f}</div>`;
        }).join('');

        // Agent Consensus
        const a = data.agents || data.agentConsensus || {};
        document.getElementById('agent-panel-grid').innerHTML = ['fundamental','technical','sentiment'].map(ag => {
            const agent = a[ag] || {};
            // If the format is nested objects:
            let scoreStr = "";
            let bias = "NEUTRAL";
            let thesis = "--";
            if (typeof agent.score === 'string') { // new old format
               const parts = agent.score.split('/');
               bias = parts[0].trim();
               scoreStr = agent.score;
               thesis = agent.text;
            } else {
               bias = agent.bias || 'NEUTRAL';
               scoreStr = `${bias} / ${agent.confidence||0}%`;
               thesis = agent.thesis || '--';
            }
            
            const bcls = bias==='BULLISH'?'bull':bias==='BEARISH'?'bear':'neut';
            return `<div class="agent-box"><div class="ag-n">${ag.toUpperCase()}</div><div class="ag-bias ${bcls}">${scoreStr}</div><div class="ag-t">${esc(thesis)}</div></div>`;
        }).join('');
        document.getElementById('debate-row').innerHTML = `Agents split — Supervisor resolves <span class="${scls}" style="font-weight:bold">${signal}</span>`;

        // Plays
        const plays = b.plays || data.plays || [];
        document.getElementById('plays-grid').innerHTML = plays.map(p=>playCardFree(p)).join('');

        // Trap / Edge
        document.getElementById('trap-text').textContent = b.trap || data.marketTrap || "--";
        document.getElementById('edge-text').textContent = b.edge || data.marketEdge || "--";

        // Ledger
        const ledgerRows = data.ledger || [
            {date: '2026-05-28', context: 'Fear Rises, Vol Stays Contained', signal: 'VOLATILE / OPEN'}
        ];
        document.getElementById('track-body').innerHTML = ledgerRows.map(row => {
            const isBear = row.signal.includes('BEARISH');
            const isBull = row.signal.includes('BULLISH');
            const cls = isBull ? 'bull' : (isBear ? 'bear' : 'neut');
            return `<div class="track-row"><span class="track-date">${row.date}</span><span class="track-hl">${row.context}</span><span class="track-result ${row.signal.includes('OPEN')?'open':''} ${cls}">${row.signal}</span></div>`;
        }).join('');

        // Vitals Context Grid
        const mv = data.macroVitals || [];
        if(mv.length > 0) {
            document.getElementById('context-grid').innerHTML = mv.map(c=>`<div class="ctx-box"><div class="ctx-lbl">${esc(c.label)}</div><div class="ctx-val ${c.label==='S&P 500'?'bull':c.label.includes('10Y')?'neut':'volt'}">${esc(c.value)}</div><div class="ctx-sub">${esc(c.change)}</div></div>`).join('');
        } else {
            document.getElementById('context-grid').innerHTML = [
                {l:"10Y Treasury", v:`${m.yieldVal||'4.493'}%`, s:`Prev ${m.yieldPrev||'4.558'}%`},
                {l:"DXY Dollar", v:m.dxyVal||'99.07', s:"Neutral"},
                {l:"VIX", v:m.vixVal||'17.01', s:"Implied Volatility"},
                {l:"S&P 500", v:m.spxVal||'7,519', s:m.spxChange||'+0.61%'},
                {l:"BTC DOM", v:`${m.btcDominance||'57.9'}%`, s:m.totalMarketCap||'$2.61T'},
                {l:"RECESSION", v:m.recessionProb||'N/A', s:"FRED model"}
            ].map(c=>`<div class="ctx-box"><div class="ctx-lbl">${esc(c.l)}</div><div class="ctx-val ${c.l==='S&P 500'?'bull':c.l.includes('10Y')?'neut':'volt'}">${esc(c.v)}</div><div class="ctx-sub">${esc(c.s)}</div></div>`).join('');
        }

        // Polymarket
        const od = num(m.marketOdds || data.polymarketOdds, 50);
        document.getElementById('poly-card').innerHTML = `<span class="poly-tag">PREDICTION MARKET</span><div class="poly-q">${esc(m.marketTitle||'Unavailable')}</div><div class="poly-row"><div class="poly-odds">${od}%</div><div style="flex:1"><div class="poly-track"><div class="poly-fill" style="width:${Math.max(0,Math.min(100,od))}%"></div></div></div></div>`;

        // Wires
        const wires = data.intelWires || [m.newsText || "Bond metrics flag caution parameters on duration tracking loops."];
        document.getElementById('wires-list').innerHTML = wires.map(w => `<div style="margin-bottom: 8px; border-left: 2px solid var(--s3); padding-left: 8px;">// ${esc(w)}</div>`).join('');

      } catch(e) { console.error("Data error:", e); }
    }

    loadTerminalPayload();
    setInterval(loadTerminalPayload, 30000);
  </script>
</body>
</html>"""
    
    new_html = new_html.replace('/*STYLES_PLACEHOLDER*/', styles)

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("Vanilla CSS Restoration complete.")

rebuild_spa()
