
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
  