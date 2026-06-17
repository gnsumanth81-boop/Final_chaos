function render(latest,signals){
      var m=latest.market||{};
      var b=latest.brief||{};
      var agents=latest.agents||{};
      var signal=b.signal||'NEUTRAL';
      var scls=sigCls(signal);
      var fear=num(m.fearIndex,50);
      var fearCls=fear<25?'bear':fear>60?'bull':'neut';
      var fearColor=fear<25?'var(--red)':fear>60?'var(--green)':'var(--gold)';
      var btcCls=num(m.btcChange)>=0?'bull':'bear';
      var generated=new Date(b.generated_at||Date.now());
      var dateStr=generated.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}).toUpperCase();
      var timeStr=generated.toISOString().slice(11,16)+' UTC';
      currentLine=b.chaos_line||'';

      // 5-Second Market Snapshot & Liveness Timer
      const topPlay = (b.plays && b.plays[0]) ? b.plays[0].type : 'N/A';
      const snapEl = document.getElementById('snapshot-panel');
      if (snapEl) {
        snapEl.innerHTML = `
          <div><div style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono);">REGIME</div><div style="font-weight:700; color:var(--text-pure);">${esc(b.active_regime||'NEUTRAL')}</div></div>
          <div><div style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono);">BIAS</div><div style="font-weight:700; color:var(--${scls==='bull'?'green':scls==='bear'?'red':'gold'});">${esc(signal)}</div></div>
          <div><div style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono);">CONFIDENCE</div><div style="font-weight:700; color:var(--text-bright);">${b.confidence||0}%</div><div style="font-size:0.5rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:2px;">MAC: ${(agents.fundamental&&agents.fundamental.confidence)||70} | FLO: ${(agents.technical&&agents.technical.confidence)||75}</div></div>
          <div><div style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono);">TOP PLAY</div><div style="font-weight:700; color:var(--text-bright);">${esc(topPlay)}</div></div>
          <div><div style="font-size:0.65rem; color:var(--text-muted); font-family:var(--font-mono);">LAST TOUCH</div><div style="font-weight:700; color:var(--text-bright);" id="liveness-timer">Just now</div></div>
        `;
      }
      
      if(window.livenessInterval) clearInterval(window.livenessInterval);
      const generatedAtTime = new Date(b.generated_at || Date.now()).getTime();
      window.livenessInterval = setInterval(() => {
        const diff = Math.floor((Date.now() - generatedAtTime) / 1000);
        const el = document.getElementById('liveness-timer');
        if(el) {
          if (diff < 60) el.innerText = diff + "s ago";
          else el.innerText = Math.floor(diff/60) + "m ago";
        }
      }, 1000);

      // Populating the Delta Panel
      const btcChange = parseFloat(m.btcChange || 0);
      const deltaBtcEl = document.getElementById('delta-btc');
      if (deltaBtcEl) {
        deltaBtcEl.innerHTML = 'BTC: ' + (btcChange >= 0 ? '+' : '') + btcChange.toFixed(2) + '%';
        deltaBtcEl.style.color = btcChange >= 0 ? 'var(--green)' : 'var(--red)';
      }
      // Update Final Chaos Bias section
      const finalBiasEl = document.getElementById('final-chaos-bias');
      const finalConfEl = document.getElementById('final-chaos-conf');
      if (finalBiasEl && finalConfEl) {
        finalBiasEl.textContent = signal;
        finalBiasEl.style.color = 'var(--' + (scls === 'bull' ? 'green' : scls === 'bear' ? 'red' : 'gold') + ')';
        finalConfEl.textContent = (b.confidence || 0) + '% CONFIDENCE';
      }
      
      const prevFear = parseFloat(m.fearPrev || m.fearIndex || 50);
      const fearShift = fear - prevFear;
      const deltaFearEl = document.getElementById('delta-fear');
      if (deltaFearEl) {
        deltaFearEl.innerHTML = 'FEAR SHIFT: ' + (fearShift > 0 ? '+' : '') + fearShift.toFixed(0);
      }

      // OG Tags
      if(document.getElementById('og-title'))document.getElementById('og-title').content='CHAOS. | '+(b.headline||'Live Brief');
      if(document.getElementById('tw-title'))document.getElementById('tw-title').content='CHAOS. | '+(b.headline||'Live Brief');
      if(document.getElementById('og-desc'))document.getElementById('og-desc').content=b.chaos_line||'';
      if(document.getElementById('tw-desc'))document.getElementById('tw-desc').content=b.chaos_line||'';

      // Ticker
      var tickerItems=[
        ['FEAR',m.fearIndex,fearCls],['BTC',m.btcPrice,btcCls],['24H',num(m.btcChange).toFixed(2)+'%',btcCls],
        ['SIGNAL',signal,scls],['CONF',(b.confidence||0)+'%','neut'],['FORCES',(b.forces||[]).length+'/9','bear'],
        ['10Y',(m.yieldVal||'N/A')+'%',num(m.yieldVal)>4.5?'bear':'neut'],['DXY',m.dxyVal||'N/A','neut'],[dateStr,'','']
      ];
      var tk=tickerItems.map(function(t){return'<span class="tk">'+esc(t[0])+' '+(t[1]?'<span class="v '+t[2]+'">'+esc(t[1])+'</span>':'')+'</span>';}).join('');
      document.getElementById('ticker-inner').innerHTML=tk+tk;

      // Header
      document.getElementById('terminal-status').textContent=dateStr+' · '+timeStr;
      document.getElementById('date-line').textContent=dateStr+' · '+timeStr+' · CHAOS INTELLIGENCE';
      var sessionBadge = document.getElementById('session-badge');
      if (sessionBadge) sessionBadge.textContent=(m.session||'MORNING')+' BRIEF';
      document.getElementById('hash-val').textContent=latest.signal?.signal_hash||'Hash pending...';

      // Vitals
      var perf = latest.performance || {};
      var tr = perf.total_resolved || 0;
      var wrText = tr < 10 ? 'CALIBRATING...' : (perf.win_rate || 0) + '%';
      var wrSubText = tr < 10 ? tr + '/10 SIGNALS' : (perf.current_streak || 0) + ' ' + (perf.streak_direction || 'WIN') + ' STREAK';

      // Ledger tab updates
      document.getElementById('ledger-win-rate').textContent = tr < 10 ? 'CALIBRATING...' : (perf.win_rate || 0) + '%';
      document.getElementById('ledger-win-rate').style.color = tr < 10 ? 'var(--gold)' : 'var(--green)';
      document.getElementById('ledger-sample-size').textContent = tr + ' resolved signals';
      document.getElementById('ledger-streak').textContent = (perf.current_streak || 0) + ' ' + (perf.streak_direction || 'WIN');
      document.getElementById('ledger-streak').style.color = perf.streak_direction === 'LOSS' ? 'var(--red)' : 'var(--green)';

      // Brief Header
      var topConfText = tr < 10 ? 'CALIBRATING ('+tr+'/10 SIGNALS)' : perf.win_rate + '% VERIFIED WR · ' + perf.current_streak + ' ' + (perf.streak_direction || 'WIN') + ' STREAK';
      document.getElementById('brief-tag').textContent='TODAY\'S BRIEFING · '+(b.dateline||'NYC').toUpperCase();
      document.getElementById('headline').textContent=b.headline||'Market Update';
      document.getElementById('sig-row').innerHTML='<span class="sig '+scls+'">'+esc(signal)+'</span><span class="ts-badge">'+esc(b.time_sensitivity||'THIS WEEK')+'</span><span class="conf">'+esc(topConfText)+'</span>';
      document.getElementById('updated-line').textContent=timeStr+' · ∞ BRAIN + LIVE DATA';

      var btcChangeVal = num(m.btcChange).toFixed(2);
      var btcSign = num(m.btcChange) >= 0 ? '▲ +' : '▼ ';
      var vitalsEl = document.getElementById('vitals-target');
      if (vitalsEl) {
        vitalsEl.innerHTML=`
          <div class="vitals-ribbon">
            <div class="v-ribbon-cell">
              <span class="v-cell-lbl">MATRIX VOLATILITY (CVX)</span>
              <span class="v-cell-val terminal-num">73.9</span>
              <span class="v-cell-delta txt-gold">● STRESSED</span>
            </div>
            <div class="v-ribbon-cell">
              <span class="v-cell-lbl">BITCOIN TARGET SPOT</span>
              <span class="v-cell-val terminal-num">${esc(m.btcPrice||'N/A')}</span>
              <span class="v-cell-delta ${btcCls}">${btcSign}${Math.abs(btcChangeVal)}%</span>
            </div>
            <div class="v-ribbon-cell">
              <span class="v-cell-lbl">ALGORITHMIC BIND VERDICT</span>
              <span class="v-cell-val terminal-num" style="color: var(--gold);">${esc(signal)}</span>
              <span class="v-cell-delta" style="color: var(--muted)">CONVICTION: ${esc(b.confidence||0)}%</span>
            </div>
            <div class="v-ribbon-cell">
              <span class="v-cell-lbl">GLOBAL SENTIMENT COMPASS</span>
              <span class="v-cell-val ${fearCls} terminal-num">${esc(m.fearIndex||'N/A')}</span>
              <span class="v-cell-delta ${fearCls}">${esc(m.fearLabel||'NEUTRAL').toUpperCase()}</span>
            </div>
          </div>
        `;
      }

      // Brief Header
      document.getElementById('brief-tag').textContent='TODAY\'S BRIEFING · '+(b.dateline||'NYC').toUpperCase();
      document.getElementById('headline').textContent=b.headline||'Market Update';
      document.getElementById('sig-row').innerHTML='<span class="sig '+scls+'">'+esc(signal)+'</span><span class="ts-badge">'+esc(b.time_sensitivity||'THIS WEEK')+'</span><span class="conf">'+esc(b.confidence||0)+'% AI CONFIDENCE · '+(b.forces||[]).length+'/9 FORCES</span>';
      document.getElementById('updated-line').textContent=timeStr+' · ∞ BRAIN + LIVE DATA';

      // Gauge animation deferred to loadData

      // Intelligence Panes
      pane('eli5','ELI5 — FOR EVERYONE','3 MIN',b.eli5,[['Fear Index',m.fearIndex],['Bitcoin',m.btcPrice],['10Y Yield',(m.yieldVal||'N/A')+'%']]);
      pane('analyst','ANALYST — INTERMEDIATE','5 MIN',b.analyst,[['10Y Treasury',(m.yieldVal||'N/A')+'%'],['DXY',m.dxyVal],['S&P 500',m.spxVal]]);
      pane('quant','QUANT — ADVANCED','7 MIN',b.quant,[['VIX',m.vixVal],['ETH',m.ethPrice],['Sentiment',m.wsbSentiment]]);

      // Forces
      var active=new Set((b.forces||[]).map(function(x){return String(x).toUpperCase();}));
      document.getElementById('forces-grid').innerHTML=ALL_FORCES.map(function(f){return'<div class="fc '+(active.has(f)?'on':'')+'"><span class="fc-dot"></span>'+FI[f]+' <span>'+f+'</span></div>';}).join('');

      // Agent Consensus
      var acEl = document.getElementById('agent-consensus');
      if (acEl) {
        var hasGeo = agents.geopolitical && agents.geopolitical.bias;
        var cols = hasGeo ? 4 : 3;
        var geoCard = hasGeo ? agentCard('Geopolitical', agents.geopolitical) : '';
        acEl.innerHTML='<div class="sec-title">🤖 AGENT CONSENSUS</div><div class="agent-panel" style="grid-template-columns:repeat('+cols+',1fr)">'+agentCard('Fundamental',agents.fundamental)+agentCard('Technical',agents.technical)+agentCard('Sentiment',agents.sentiment)+geoCard+'</div><div style="text-align:center"><span class="debate-badge">'+esc(b.agent_consensus?.debate_required?'DEBATE RESOLVED':'✓ UNANIMOUS')+'</span></div>';
      }

      // Chaos Line
      var clEl = document.getElementById('chaos-line-card');
      if (clEl) {
        clEl.innerHTML='<span class="chaos-tag">✦ THE CHAOS LINE</span><div class="chaos-text" id="chaos-quote-text">&ldquo;'+esc(b.chaos_line||'')+'&rdquo;</div><div class="share-row"><a class="btn btn-secondary" target="_blank" href="https://twitter.com/intent/tweet?text='+encodeURIComponent('"'+(b.chaos_line||'')+'" — Chaos Intelligence\n'+SITE)+'">𝕏 Post</a><a class="btn btn-secondary" target="_blank" href="https://t.me/share/url?url='+encodeURIComponent(SITE)+'&text='+encodeURIComponent('"'+(b.chaos_line||'')+'" — Chaos Intelligence')+'">✈ Telegram</a><button class="btn btn-secondary" onclick="copyLine()">📋 Copy Line</button><button class="btn btn-secondary" style="color:var(--gold);" onclick="generateChaosImage()">🖼️ Download Image</button></div>';
      }

      // Trap
      var tpEl = document.getElementById('trap-card');
      if (tpEl) {
        tpEl.innerHTML='<div class="trap-tag">⚠ MARKET TRAP</div><div class="trap-text">'+briefHtml(b.trap)+'</div>';
      }

      // Edge
      var edEl = document.getElementById('edge-card');
      if (edEl) {
        edEl.innerHTML='<div class="edge-tag">🔍 THE EDGE — WHAT OTHERS ARE MISSING</div><div class="edge-text">'+briefHtml(b.edge)+'</div>';
      }

      // Plays
      document.getElementById('plays-grid').innerHTML=(b.plays||[]).map(playCard).join('');

      // Ledger
      document.getElementById('ledger').innerHTML=renderLedger(signals);

      // Macro Grid
      // Polymarket Matrix rendering
      const polyCard = document.getElementById('poly-card');
      if (polyCard) {
        let isUnavailable = false;
        const mTitle = m.marketTitle || '';
        if (!b.extendedPolymarketVitals && (!mTitle || mTitle.includes('unavailable'))) {
          isUnavailable = true;
        }

        if (isUnavailable) {
          polyCard.style.display = 'none';
        } else {
          polyCard.style.display = 'block';
          if (b.extendedPolymarketVitals) {
            const pData = b.extendedPolymarketVitals;
            const labelsMap = {
              fedRateCut: "Fed Rate Cut Next Session",
              usElection: "US Presidential Futures",
              globalConflict: "Cross-Border Sovereign Flashpoint",
              gazaCeasefire: "Geopolitical Ceasefire Resolution"
            };
            
            let matrixHtml = '<span class="poly-tag" style="display:flex;justify-content:space-between;"><span>⚡ LIVE POLYMARKET CLOB TELEMETRY MATRIX</span><span style="color:var(--green);animation:pulse 2s infinite">● FEED_LIVE</span></span><div style="margin-top:16px;display:flex;flex-direction:column;gap:12px;">';
            for (const [key, value] of Object.entries(pData)) {
              const label = labelsMap[key] || key;
              matrixHtml += `
                <div style="display:flex;flex-direction:column;gap:6px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;font-family:var(--font-mono);font-size:0.65rem;text-transform:uppercase;">
                    <span style="color:var(--ink);">${esc(label)}</span>
                    <span style="color:var(--blue);font-weight:700;">${esc(value)}% PROBABILITY</span>
                  </div>
                  <div class="poly-track" style="height:4px;">
                    <div class="poly-fill" style="width:${Math.max(0,Math.min(100,value))}%;background:linear-gradient(90deg,var(--blue),var(--red));"></div>
                  </div>
                </div>
              `;
            }
            matrixHtml += '</div>';
            polyCard.innerHTML = matrixHtml;
          } else {
            const odds=num(m.marketOdds,50);
            polyCard.innerHTML='<span class="poly-tag">⚡ TOP PREDICTION MARKET</span><div class="poly-q">'+esc(m.marketTitle||'Prediction market unavailable')+'</div><div class="poly-row"><div class="poly-odds">'+esc(m.marketOdds||'50.0')+'%</div><div><div style="font-family:var(--font-mono);font-size:.44rem;color:var(--muted);margin-bottom:6px">YES probability</div><div class="poly-track"><div class="poly-fill" style="width:'+Math.max(0,Math.min(100,odds))+'%"></div></div></div></div><div style="margin-top:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px"><div class="vd">Volume: '+esc(m.marketVolume||'$0')+'</div><a class="poly-link" href="'+esc(m.marketLink||'https://polymarket.com')+'" target="_blank">VIEW LIVE →</a></div>';
          }
        }
      }
      document.getElementById('macro-grid').innerHTML=[
        metric('10Y Treasury',(m.yieldVal||'N/A')+'%','Yield change',num(m.yieldVal)>4.5?'bear':'neut'),
        metric('DXY Dollar',m.dxyVal||'N/A',num(m.dxyVal)>104?'↑ EM pressure':'— Neutral','neut'),
        metric('VIX',m.vixVal||'N/A','Implied vol',num(m.vixVal)>20?'bear':'neut'),
        metric('S&P 500',m.spxVal||'N/A',m.spxChange||'',String(m.spxChange||'').startsWith('+')?'bull':'bear'),
        metric('Recession Prob',m.recessionProb||'N/A','FRED/NY Fed model','neut'),
        metric('BTC Dominance',m.btcDominance||'N/A',m.totalMarketCap||'Crypto MCap','neut'),
        metric('Gold /oz',m.goldPrice||'N/A','Safe-haven demand','neut'),
        metric('WSB Sentiment',m.wsbSentiment||'N/A','Retail positioning',m.wsbSentiment==='BULLISH'?'bull':m.wsbSentiment==='BEARISH'?'bear':'neut')
      ].join('');

      // Context
      document.getElementById('context-grid').innerHTML=renderContext(m,b);

      // Wires
      const wiresEl = document.getElementById('wires');
      if (wiresEl) {
        if (!b.news_wires || b.news_wires.length === 0) {
          wiresEl.parentElement.style.display = 'none';
        } else {
          wiresEl.parentElement.style.display = 'block';
          wiresEl.innerHTML = renderWires(b.news_wires);
        }
      }

      // ══ CVX ENGINE ══
      var cvxFear = num(m.fearIndex, 50);
      var cvxVix = num(m.vixVal, 15);
      var geoBias = (agents.geopolitical && agents.geopolitical.bias) ? String(agents.geopolitical.bias).toUpperCase() : 'NEUTRAL';
      var geoMod = geoBias === 'ELEVATED' ? 15 : geoBias === 'CRITICAL' ? 25 : geoBias === 'BEARISH' ? 12 : 5;
      var cvxScore = Math.min(100, Math.max(10, Math.round((cvxFear * 0.35) + (cvxVix * 1.8) + geoMod)));

      // Apply regime tint
      document.body.classList.remove('defcon-calm', 'defcon-stressed', 'defcon-chaos');
      var cvxRegime, cvxCls;
      if (cvxScore >= 80) { document.body.classList.add('defcon-chaos'); cvxRegime = 'CHAOS REGIME'; cvxCls = 'cvx-chaos'; }
      else if (cvxScore >= 55) { document.body.classList.add('defcon-stressed'); cvxRegime = 'STRESSED REGIME'; cvxCls = 'cvx-stressed'; }
      else { document.body.classList.add('defcon-calm'); cvxRegime = 'CALM REGIME'; cvxCls = 'cvx-calm'; }

      // Header CVX badge
      var hdrCvx = document.getElementById('hdr-cvx');
      if (hdrCvx) { hdrCvx.textContent = cvxScore; hdrCvx.className = 'hdr-cvx-num ' + cvxCls; }

      // ══ MOBILE SIGNAL CARD POPULATION ══
      var perf = latest.performance || {};
      var mHash = document.getElementById('m-hash');
      if (mHash) mHash.textContent = latest.signal && latest.signal.signal_hash ? latest.signal.signal_hash.substring(0, 12) : '';

      var mCvx = document.getElementById('m-cvx-num');
      if (mCvx) mCvx.textContent = cvxScore;
      var mRegime = document.getElementById('m-regime-txt');
      if (mRegime) { mRegime.textContent = cvxRegime; mRegime.style.color = cvxCls === 'cvx-chaos' ? 'var(--red)' : cvxCls === 'cvx-stressed' ? 'var(--gold)' : 'var(--green)'; }

      var mHeadline = document.getElementById('m-headline');
      if (mHeadline) mHeadline.textContent = b.headline || 'Market Update';
      var mChaosLine = document.getElementById('m-chaos-line');
      if (mChaosLine) mChaosLine.textContent = b.chaos_line ? '\u201c' + b.chaos_line + '\u201d' : '';

      var mWr = document.getElementById('m-wr-val');
      if (mWr) { var wr = perf.win_rate || 0; var tr = perf.total_resolved || 0; mWr.textContent = tr > 0 ? wr + '% (' + tr + ' signals)' : 'CALIBRATING'; }

      var mPlays = document.getElementById('m-plays');
      if (mPlays) {
        var plays = b.plays || [];
        var borders = ['border-safe', 'border-stressed', 'border-chaos'];
        var badges = ['\ud83d\udee1\ufe0f SAFE', '\u26a1 AGGRES', '\ud83d\udd04 CONTRA'];
        var colors = ['txt-green', 'txt-gold', 'txt-red'];
        mPlays.innerHTML = plays.map(function(p, i) {
          return '<div class="m-track-row ' + (borders[i] || '') + '"><div class="m-track-meta"><span class="m-badge-type ' + (colors[i] || '') + '">' + (badges[i] || p.type) + '</span><span class="m-track-asset">' + esc(p.thesis || '').substring(0, 30) + '</span></div><div class="m-track-details">' + esc(p.details || '') + '</div></div>';
        }).join('');
      }

      var mDecayTxt = document.getElementById('m-decay-txt');
      if (mDecayTxt) mDecayTxt.textContent = 'VALID — ' + esc(b.time_sensitivity || 'THIS WEEK');
      var mDecayFill = document.getElementById('m-decay-fill');
      if (mDecayFill) {
        var ts = String(b.time_sensitivity || '').toUpperCase();
        var w = ts === 'IMMEDIATE' ? 25 : ts === 'TODAY' ? 60 : 100;
        mDecayFill.style.width = w + '%';
        if (w <= 25) mDecayFill.classList.add('decay-critical'); else mDecayFill.classList.remove('decay-critical');
      }

      // Reveal & Clock
      reveal();
      updateWorldClock();
    }