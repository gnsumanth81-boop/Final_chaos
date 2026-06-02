
    // ═══════════════════════════════════════════
    // SPA ROUTER (new)
    // ═══════════════════════════════════════════
    function runClientRouter() {
      const hash = window.location.hash || '#terminal';
      const targets = { '#terminal': 'view-terminal', '#ledger': 'view-ledger', '#vitals': 'view-vitals', '#alpha': 'view-alpha' };
      const viewId = targets[hash] || 'view-terminal';
      document.querySelectorAll('.spa-view').forEach(v => v.classList.remove('active'));
      const el = document.getElementById(viewId);
      if (el) el.classList.add('active');
      document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('data-target') === viewId);
      });
      window.scrollTo(0, 0);
    }
    window.addEventListener('hashchange', runClientRouter);
    window.addEventListener('load', runClientRouter);

    // ═══════════════════════════════════════════
    // ORIGINAL JS (untouched from index.backup.html)
    // ═══════════════════════════════════════════

    const API_LATEST = './api/latest.json';
    const API_SIGNALS = './api/signals.json';
    const ALL_FORCES = ['MONEY','TECH','ENERGY','POLITICS','WAR','DEBT','JOBS','FOOD','PEOPLE'];
    const FI = {MONEY:'$',TECH:'AI',ENERGY:'E',POLITICS:'P',WAR:'W',DEBT:'D',JOBS:'J',FOOD:'F',PEOPLE:'H'};
    const SITE = 'https://chaos.sumanthworks.com';
    let currentLine = '';

    function esc(s){return String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
    function num(v,f=0){const n=parseFloat(String(v??'').replace(/[^0-9.-]/g,''));return Number.isFinite(n)?n:f}
    function sigCls(s){return s==='BULLISH'?'bull':s==='BEARISH'?'bear':s==='VOLATILE'?'volt':'neut'}
    function biasCls(s){return s==='BULLISH'?'bull':s==='BEARISH'?'bear':'neut'}
    function briefHtml(text){const parts=String(text||'No data available.').split(/\n\n+/).filter(Boolean);return parts.map(p=>`<p>${esc(p)}</p>`).join('')}
    function metric(label,val,sub,cls='neut'){return `<div class="mi"><div class="mi-l">${esc(label)}</div><div class="mi-v ${cls}">${esc(val)}</div><div class="mi-s">${esc(sub)}</div></div>`}
    function vital(label,val,sub,cls='neut'){return `<div class="vital"><div class="vv ${cls}">${esc(val)}</div><div class="vl">${esc(label)}</div><div class="vd">${esc(sub)}</div></div>`}

    async function loadData(){
      const [latestRes, signalsRes] = await Promise.all([fetch(API_LATEST,{cache:'no-store'}), fetch(API_SIGNALS,{cache:'no-store'})]);
      const latest = await latestRes.json();
      const signals = await signalsRes.json();
      render(latest, signals);
    }

    function render(latest, signals){
      const m = latest.market || {};
      const b = latest.brief || {};
      const agents = latest.agents || {};
      const signal = b.signal || 'NEUTRAL';
      const scls = sigCls(signal);
      const btcCls = num(m.btcChange) >= 0 ? 'bull' : 'bear';
      const fear = num(m.fearIndex, 50);
      const fearCls = fear < 25 ? 'bear' : fear > 60 ? 'bull' : 'neut';
      const fearColor = fear < 25 ? 'var(--red)' : fear > 60 ? 'var(--green)' : 'var(--gold)';
      const generated = new Date(b.generated_at || latest.signal?.timestamp || Date.now());
      const dateStr = generated.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}).toUpperCase();
      const timeStr = generated.toISOString().slice(11,16) + ' UTC';
      currentLine = b.chaos_line || '';

      const tickerItems = [
        ['FEAR', m.fearIndex, fearCls], ['BTC', m.btcPrice, btcCls], ['24H', `${num(m.btcChange).toFixed(2)}%`, btcCls],
        ['SIGNAL', signal, scls], ['CONF', `${b.confidence || 0}%`, 'neut'], ['FORCES', `${(b.forces||[]).length}/9`, 'bear'],
        ['10Y', `${m.yieldVal || 'N/A'}%`, num(m.yieldVal) > 4.5 ? 'bear' : 'neut'], ['DXY', m.dxyVal || 'N/A', 'neut'], ['CVX', `${m.cvxScore || 'N/A'}`, 'volt'], [dateStr,'','']
      ];
      const tk = tickerItems.map(([k,v,c])=>`<span class="tk">${esc(k)} ${v?`<span class="v ${c}">${esc(v)}</span>`:''}</span>`).join('');
      document.getElementById('ticker-inner').innerHTML = tk + tk;
      
      const hd = b.headline || 'Live Brief';
      const cl = b.chaos_line || 'Chaos Intelligence live macro war-room brief.';
      if(document.getElementById('og-title')) document.getElementById('og-title').content = `CHAOS. | ${hd}`;
      if(document.getElementById('tw-title')) document.getElementById('tw-title').content = `CHAOS. | ${hd}`;
      if(document.getElementById('og-desc')) document.getElementById('og-desc').content = cl;
      if(document.getElementById('tw-desc')) document.getElementById('tw-desc').content = cl;

      document.getElementById('date-line').textContent = `${dateStr} - ${timeStr} - CHAOS INTELLIGENCE`;
      document.getElementById('session-badge').textContent = `${m.session || 'DAILY'} BRIEF`;
      document.getElementById('hash-val').textContent = latest.signal?.signal_hash || 'Hash pending...';
      document.getElementById('vitals').innerHTML = [
        vital('Fear Index', m.fearIndex || 'N/A', `${m.fearLabel || ''} ${m.fearDelta ? '(' + (m.fearDelta > 0 ? '+' : '') + m.fearDelta + ')' : ''}`, fearCls),
        vital('BTC/USD', m.btcPrice || 'N/A', `24h ${num(m.btcChange).toFixed(2)}%`, btcCls),
        vital('Signal', signal, 'AI model', scls),
        vital('Confidence', `${b.confidence || 0}%`, 'live brief', 'neut')
      ].join('');
      document.getElementById('brief-tag').textContent = `TODAY'S BRIEFING - ${(b.dateline || 'GLOBAL').toUpperCase()}`;
      document.getElementById('headline').textContent = b.headline || 'Market Update';
      document.getElementById('sig-row').innerHTML = `<span class="sig ${scls}">${esc(signal)}</span><span class="ts-badge">${esc(b.time_sensitivity || 'THIS WEEK')}</span><span class="conf">${esc(b.confidence || 0)}% AI CONFIDENCE - ${(b.forces||[]).length}/9 FORCES</span>`;
      document.getElementById('updated-line').textContent = `${timeStr} - LIVE DATA - ${m.label || ''}`;

      document.getElementById('gauge-arc').setAttribute('stroke', fearColor);
      document.getElementById('gauge-glow').style.background = fearColor;
      document.getElementById('gauge-num').className = `gauge-val ${fearCls}`;
      document.getElementById('gauge-label').textContent = String(m.fearLabel || 'Neutral').toUpperCase();
      setTimeout(()=>animateGauge(fear), 120);

      pane('eli5', 'ELI5 - FOR EVERYONE', '3 MIN', b.eli5, [
        ['Fear Index', m.fearIndex], ['Bitcoin', m.btcPrice], ['10Y Yield', `${m.yieldVal || 'N/A'}%`]
      ]);
      pane('analyst', 'ANALYST - INTERMEDIATE', '5 MIN', b.analyst, [
        ['10Y Treasury', `${m.yieldVal || 'N/A'}%`], ['DXY', m.dxyVal], ['S&P 500', m.spxVal]
      ]);
      pane('quant', 'QUANT - ADVANCED', '7 MIN', b.quant, [
        ['VIX', m.vixVal], ['ETH', m.ethPrice], ['CVX', m.cvxScore]
      ]);

      const active = new Set((b.forces || []).map(x=>String(x).toUpperCase()));
      document.getElementById('forces-grid').innerHTML = ALL_FORCES.map(f=>`<div class="fc ${active.has(f)?'on':''}"><span class="fc-dot"></span>${FI[f]} <span>${f}</span></div>`).join('');

      document.getElementById('agent-consensus').innerHTML = `
        <div class="sec-title">AGENT CONSENSUS</div>
        <div class="agent-panel">
          ${agentCard('Fundamental', agents.fundamental)}
          ${agentCard('Technical', agents.technical)}
          ${agentCard('Sentiment', agents.sentiment)}
        </div>
        <div style="text-align:center"><span class="debate-badge">${esc(b.agent_consensus?.debate_required ? 'DEBATE RESOLVED' : 'UNANIMOUS')}</span></div>
        ${b.agent_consensus?.resolution ? `<div style="font-family:var(--font-mono);font-size:.5rem;color:var(--muted);text-align:center;margin-top:8px;padding:8px;border-top:1px solid var(--s3)">${esc(b.agent_consensus.resolution)}</div>` : ''}
      `;

      document.getElementById('chaos-line-card').innerHTML = `<span class="chaos-tag">THE CHAOS LINE</span><div class="chaos-text">&ldquo;${esc(b.chaos_line || '')}&rdquo;</div><div class="share-row"><button class="s-btn red" onclick="copyLine()">Copy Line</button><a class="s-btn x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=${encodeURIComponent('"' + (b.chaos_line || '') + '" - Chaos Intelligence\\n' + SITE)}">X Post</a><button class="s-btn ghost" onclick="window.scrollTo({top:0,behavior:'smooth'})">Top</button></div>`;

      document.getElementById('ledger').innerHTML = renderLedger(signals);
      document.getElementById('macro-grid').innerHTML = [
        metric('10Y Treasury', `${m.yieldVal || 'N/A'}%`, `Prev ${m.yieldPrev || 'N/A'}%`, num(m.yieldVal) > 4.5 ? 'bear' : 'neut'),
        metric('DXY Dollar', m.dxyVal || 'N/A', num(m.dxyVal) > 104 ? 'EM pressure' : 'Neutral', 'neut'),
        metric('VIX', m.vixVal || 'N/A', 'Implied vol', num(m.vixVal) > 20 ? 'bear' : 'neut'),
        metric('S&P 500', m.spxVal || 'N/A', m.spxChange || '', String(m.spxChange||'').startsWith('+') ? 'bull' : 'bear'),
        metric('BTC Dominance', m.btcDominance || 'N/A', m.totalMarketCap || 'Crypto MCap', 'neut'),
        metric('Recession Prob', m.recessionProb || 'N/A', 'FRED/NY Fed model', 'neut')
      ].join('');

      document.getElementById('trap-card').innerHTML = `<div class="trap-tag">MARKET TRAP</div><div class="trap-text">${briefHtml(b.trap)}</div>`;
      document.getElementById('edge-card').innerHTML = `<div class="edge-tag">THE EDGE - WHAT OTHERS ARE MISSING</div><div class="edge-text">${briefHtml(b.edge)}</div>`;
      document.getElementById('plays-grid').innerHTML = (b.plays || []).map(playCard).join('');
      document.getElementById('wires').innerHTML = renderWires(b.news_wires, m.newsText);
      document.getElementById('context-grid').innerHTML = renderContext(m, b);
      const odds = num(m.marketOdds, 50);
      document.getElementById('poly-card').innerHTML = `<span class="poly-tag">TOP PREDICTION MARKET</span><div class="poly-q">${esc(m.marketTitle || 'Prediction market unavailable')}</div><div class="poly-row"><div class="poly-odds">${esc(m.marketOdds || '50.0')}%</div><div style="flex:1"><div class="poly-track"><div class="poly-fill" style="width:${Math.max(0,Math.min(100,odds))}%"></div></div></div></div><div style="margin-top:14px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap"><div class="vd">Volume: ${esc(m.marketVolume || '$0')}</div><a class="poly-link" href="${esc(m.marketLink || 'https://polymarket.com')}" target="_blank" rel="noopener">VIEW LIVE</a></div>`;

      reveal();
      updateWorldClock();
    }

    function pane(id, tag, time, text, metrics){
      document.getElementById(`pane-${id}`).innerHTML = `<div class="brief"><div class="brief-meta"><span class="brief-tag">${esc(tag)}</span><span class="brief-tag">${esc(time)}</span><button class="voice-btn" onclick="chaosSpeak('pane-${id}',this)">LISTEN</button></div>${briefHtml(text)}<div class="brief-metrics">${metrics.map(([l,v])=>`<div class="bm"><div class="bm-v">${esc(v ?? 'N/A')}</div><div class="bm-l">${esc(l)}</div></div>`).join('')}</div></div>`;
    }
    function agentCard(name,a={}){return `<div class="agent-card"><div class="agent-name">${esc(name)}</div><div class="agent-bias ${biasCls(a.bias)}">${esc(a.bias || 'NEUTRAL')} / ${esc(a.confidence || 0)}%</div><div class="agent-thesis">${esc(a.thesis || 'Awaiting agent output.')}</div></div>`}
    function playCard(p){const inner=`<div class="play-card-type ${p.type==='SAFE'?'bull':p.type==='AGGRESSIVE'?'bear':'neut'}">${esc(p.type)}</div><div class="play-card-thesis">${esc(p.thesis)}</div><div class="play-card-details">${briefHtml(p.details)}</div>`;return `<div class="play-card">${inner}</div>`}
    function renderLedger(signals){if(!signals?.length)return '<div class="vd">No signals logged yet.</div>';return signals.slice(0,7).map(s=>`<div class="ledger-row"><span>${esc(new Date(s.timestamp).toISOString().slice(0,10))} - ${esc(s.headline)}</span><span class="${sigCls(s.signal)}">${esc(s.signal)} / ${esc(s.resolved ? s.result : 'OPEN')}</span></div>`).join('')}
    function renderWires(newsWires, newsText){const wires = Array.isArray(newsWires)&&newsWires.length ? newsWires : String(newsText||'').split('\n').filter(Boolean).slice(0,4).map((t,i)=>({source:'WIRE',title:t,impact:'Market impact pending AI wire synthesis.'})); if(!wires.length)return '<div class="wire"><div class="wire-hl" style="color:var(--muted)">No wires this session.</div></div>';return wires.map((w,i)=>`<div class="wire" onclick="this.classList.toggle('open')"><span class="wire-src">${esc(w.source||'WIRE')}</span><div class="wire-hl">${esc(w.title||'Untitled')}</div><div class="wire-body">${esc(w.impact||'No impact note.')}</div></div>`).join('')}
    function renderContext(m,b){const bond=num(m.yieldVal)>4.5?'RISK':num(m.yieldVal)>4?'CAUTION':'CALM';const equity=String(m.spxChange||'').startsWith('+')?'BULLISH':'CAUTION';const crypto=num(m.btcChange)>2?'RALLY':num(m.btcChange)<-2?'SELLOFF':'HEDGING';const sent=`FEAR ${m.fearIndex||'N/A'}`;const rows=[['Bond Market',bond,`10Y at ${m.yieldVal||'N/A'}%`,bond==='RISK'?'var(--red)':'var(--gold)'],['Equity Market',equity,`S&P 500 ${m.spxChange||'flat'}`,equity==='BULLISH'?'var(--green)':'var(--gold)'],['Crypto',crypto,`BTC at ${m.btcPrice||'N/A'} (${m.btcChange||'0'}%)`,'var(--gold)'],['Sentiment',sent,`${m.fearLabel||'Neutral'} sentiment`,'var(--purple)']];return rows.map(([l,v,d,a])=>`<div class="ctx-card" style="--accent:${a}"><div class="ctx-l">${esc(l)}</div><div class="ctx-v ${v==='BULLISH'||v==='RALLY'?'bull':v==='RISK'||v==='SELLOFF'?'bear':'neut'}">${esc(v)}</div><div class="ctx-d">${esc(d)}</div></div>`).join('')}
    function animateGauge(target){const arc=document.getElementById('gauge-arc'),numEl=document.getElementById('gauge-num');const total=251;arc.style.strokeDashoffset=total-(target/100)*total;let n=0;const step=Math.max(1,Math.round(target/36));const iv=setInterval(()=>{n+=step;if(n>=target){n=target;clearInterval(iv)}numEl.textContent=n},20)}
    function setCx(cx,btn){if(window.speechSynthesis)speechSynthesis.cancel();document.querySelectorAll('.voice-btn').forEach(b=>b.classList.remove('playing'));document.querySelectorAll('.cx-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));btn.classList.add('active');document.getElementById('pane-'+cx).classList.add('active')}
    
    window.findVoice = function(patterns) {
      const vs = speechSynthesis.getVoices();
      for (const p of patterns) {
        const v = vs.find(x => p.test(x.name));
        if (v) return v;
      }
      return vs.find(x => /en-(US|GB)/i.test(x.lang)) || vs[0];
    };

    function chaosSpeak(paneId, btn) {
      if (!('speechSynthesis' in window)) return;
      if (btn.classList.contains('playing')) {
        speechSynthesis.cancel();
        btn.classList.remove('playing');
        btn.textContent = 'LISTEN';
        return;
      }
      document.querySelectorAll('.voice-btn').forEach(b => {
        b.classList.remove('playing');
        b.textContent = 'LISTEN';
      });
      const text = document.getElementById(paneId)?.innerText.replace(/\s+/g, ' ').trim();
      if (!text) return;
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-US';
      
      if (paneId.includes('eli5')) {
        u.rate = 1.0; u.pitch = 1.2;
        u.voice = window.findVoice([/Samantha/i, /Victoria/i, /Google US English/i, /Zira/i]);
      } else if (paneId.includes('quant')) {
        u.rate = 1.25; u.pitch = 0.9;
        u.voice = window.findVoice([/Fred/i, /Ralph/i, /Albert/i, /Microsoft Mark/i, /Richard/i, /Google UK/i]);
      } else {
        u.rate = 1.0; u.pitch = 1.0;
        u.voice = window.findVoice([/Guy Online/i, /Ryan Online/i, /Google UK English Male/i, /Daniel/i, /Microsoft Richard/i, /Microsoft George/i, /Male/i]);
      }
      
      btn.classList.add('playing');
      btn.textContent = 'PLAYING';
      u.onend = () => {
        btn.classList.remove('playing');
        btn.textContent = 'LISTEN';
      };
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
    }
    
    if ('speechSynthesis' in window) {
      speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
    }

    function copyLine(){navigator.clipboard?.writeText(`"${currentLine}" - Chaos Intelligence\n${SITE}`)}
    function updateWorldClock(){const bar=document.getElementById('world-clock-bar');if(!bar)return;const now=new Date();const h=now.getUTCHours();const session=h<7?'ASIA SESSION':h<13?'EUROPE SESSION':'US SESSION';function tz(z){return now.toLocaleTimeString('en-US',{timeZone:z,hour:'2-digit',minute:'2-digit',hour12:false})}bar.innerHTML=`<span class="wc-item"><strong>${session}</strong></span><span class="wc-item">UTC <span class="wc-time">${tz('UTC')}</span></span><span class="wc-item">NY <span class="wc-time">${tz('America/New_York')}</span></span><span class="wc-item">LDN <span class="wc-time">${tz('Europe/London')}</span></span><span class="wc-item">MUM <span class="wc-time">${tz('Asia/Kolkata')}</span></span><span class="wc-item">TKY <span class="wc-time">${tz('Asia/Tokyo')}</span></span>`}
    function reveal(){const rvs=document.querySelectorAll('.rv');const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');obs.unobserve(e.target)}}),{threshold:.06,rootMargin:'0px 0px -30px 0px'});rvs.forEach(r=>obs.observe(r))}
    window.addEventListener('scroll',()=>{const h=document.documentElement;const max=h.scrollHeight-h.clientHeight;document.getElementById('progress').style.width=(max?Math.round(h.scrollTop/max*100):0)+'%'});
    window.addEventListener('load',()=>setTimeout(()=>{document.getElementById('boot').classList.add('gone');setTimeout(()=>document.getElementById('boot').style.display='none',600)},350));
    setInterval(updateWorldClock,15000);
    loadData().catch(err=>{document.getElementById('headline').textContent='Chaos Load Failed';document.getElementById('updated-line').textContent=err.message;document.getElementById('boot').classList.add('gone')});
  
  