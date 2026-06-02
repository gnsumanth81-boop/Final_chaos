import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Load current workflow
workflow_path = 'chaos_v7_complete.json'
with open(workflow_path, 'r', encoding='utf-8') as f:
    wf = json.load(f)

# The HTML Builder Node Code
html_builder_code = r"""
function safeGet(nodeName) {
  try { return $(nodeName).first().json || {}; }
  catch(e) { return {}; }
}

const d = $input.first().json;

function esc(s){ if(s==null)return''; return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }
function fmtBrief(text){ if(!text)return''; return text.split(/\n\n+/).map(p=>{ let h=esc(p).replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>'); return `<p>${h}</p>`; }).join(''); }
function fmtBriefFallback(text){ if(!text)return''; const sentences=String(text).split(/(?<=[.!?])\s+/); if(sentences.length<=3)return `<p>${esc(text)}</p>`; const mid=Math.ceil(sentences.length/2); return `<p>${esc(sentences.slice(0,mid).join(' '))}</p><p>${esc(sentences.slice(mid).join(' '))}</p>`; }
function renderBrief(text){ if(!text)return'<p>No data available.</p>'; if(text.includes('\n\n')||text.includes('**'))return fmtBrief(text); return fmtBriefFallback(text); }

const SITE='https://chaos.sumanthworks.com';
const ALL_FORCES=['MONEY','TECH','ENERGY','POLITICS','WAR','DEBT','JOBS','FOOD','PEOPLE'];
const FI={MONEY:'💰',TECH:'🤖',ENERGY:'⚡',POLITICS:'🏛️',WAR:'⚔️',DEBT:'💸',JOBS:'💼',FOOD:'🌾',PEOPLE:'🧑'};
const FD={MONEY:'Central bank policy, interest rates, and global liquidity.',TECH:'AI development, semiconductor supply chains, digital infrastructure.',ENERGY:'Oil, gas, renewable transition, energy geopolitics.',POLITICS:'Elections, regulation, government spending, fiscal policy.',WAR:'Active conflicts, sanctions, military escalations.',DEBT:'Sovereign debt, deficit spending, bond market dynamics.',JOBS:'Employment data, wage growth, labor market slack.',FOOD:'Agricultural commodity prices and food inflation.',PEOPLE:'Demographics, migration, social sentiment.'};
const FS={MONEY:'Monetary policy transmission active',TECH:'Chip war + AI investment cycle dominant',ENERGY:'Oil markets stable, no acute supply shock',POLITICS:'Fiscal policy under debate',WAR:'No new escalation this session',DEBT:'Near-record Treasury issuance',JOBS:'Labor market data inline',FOOD:'Agricultural prices stable',PEOPLE:'No acute population shock'};

const active=d.forces||['MONEY'];
const sigCls={BULLISH:'bull',BEARISH:'bear',NEUTRAL:'neut',VOLATILE:'volt'}[d.signal]||'neut';
const fearCls=d.fearIndex<25?'bear':d.fearIndex>60?'bull':'neut';
const btcCls=parseFloat(d.btcChange||0)>=0?'bull':'bear';
const now=new Date(d.generated_at||new Date());
const dateStr=now.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'}).toUpperCase();
const timeStr=now.toISOString().substring(11,16)+' UTC';
const fearDelta=d.fearDelta>0?`▲ +${d.fearDelta} vs yest`:d.fearDelta<0?`▼ ${d.fearDelta} vs yest`:'— unchanged';
const fearDeltaCls=d.fearDelta>0?'dn':d.fearDelta<0?'up':'flat';
const tweetTxt=encodeURIComponent(`"${d.chaos_line}" — Chaos Intelligence\n${SITE}`);
const tgTxt=encodeURIComponent(`"${d.chaos_line}" — Chaos Intelligence\n\n${dateStr} brief: ${SITE}`);
const fearPct=Math.min(100,Math.max(0,d.fearIndex||50));
const fearAngle=-90+(fearPct/100)*180;
const fearColor=d.fearIndex<25?'var(--red)':d.fearIndex>60?'var(--green)':'var(--gold)';

// Forces HTML
const forcesHTML=ALL_FORCES.map(f=>{
  const on=active.includes(f);
  return `<div class="fc ${on?'on':'off'}"><span class="fc-dot"></span>${FI[f]} <span class="fc-n">${f}</span><div class="fc-tip"><div class="ftt ${on?'on':'off'}">${FI[f]} ${f}</div><div class="ftd">${esc(FD[f])}</div><div class="fts ${on?'on':'off'}">${on?'⚡ ACTIVE':'○ DORMANT'} — ${esc(FS[f])}</div></div></div>`;
}).join('');

// Wires HTML
const wiresHTML=(d.news_wires||[]).map((w,i)=>{
  const wf=(Array.isArray(w.forces)?w.forces:[]).map(f=>`${FI[f]||''} ${f}`).join(' · ');
  return `<div class="wire" onclick="this.classList.toggle('open')" style="animation-delay:${i*60}ms"><div class="wire-top"><span class="wire-src">${esc(w.source)}</span><span class="wire-arr">↓</span></div><div class="wire-hl">${esc(w.title)}</div><div class="wire-peek">→ Click for market impact</div><div class="wire-body">${esc(w.impact)}${wf?`<span class="wire-ftag">Forces: ${esc(wf)}</span>`:''}</div></div>`;
}).join('');

// Macro dashboard HTML
const md=d.macro_dashboard||{};
const macroItems=[
  {label:'10Y Treasury',val:d.yieldVal?d.yieldVal+'%':md.yield_10y||'N/A',sub:md.yield_delta||'Yield change',cls:parseFloat(d.yieldVal||0)>4.5?'dn':'neut'},
  {label:'DXY Dollar',val:d.dxyVal||md.dxy||'N/A',sub:parseFloat(d.dxyVal||0)>104?'↑ EM pressure':'— Neutral',cls:parseFloat(d.dxyVal||0)>104?'dn':'neut'},
  {label:'VIX',val:d.vixVal||md.vix||'N/A',sub:'Implied vol',cls:parseFloat(d.vixVal||0)>20?'dn':parseFloat(d.vixVal||0)<15?'up':'neut'},
  {label:'S&P 500',val:d.spxVal||md.spx||'N/A',sub:d.spxChange||md.spx_delta||'',cls:(d.spxChange||'').startsWith('+')?'up':'dn'},
  {label:'Recession Prob',val:d.recessionProb||md.recession_prob||'N/A',sub:'FRED/NY Fed model',cls:parseFloat(d.recessionProb||0)>30?'dn':parseFloat(d.recessionProb||0)>15?'neut':'up'},
  {label:'BTC Dominance',val:d.btcDominance||md.btc_dominance||'N/A',sub:d.totalMarketCap||'Crypto MCap',cls:'neut'},
  {label:'WSB Sentiment',val:d.wsbSentiment||'N/A',sub:d.wsbTopTickers||'Retail positioning',cls:d.wsbSentiment==='BULLISH'?'up':d.wsbSentiment==='BEARISH'?'dn':'neut'}
];
const macroHTML=macroItems.map((m,i)=>`<div class="mi" style="animation-delay:${i*80}ms"><div class="mi-l">${esc(m.label)}</div><div class="mi-v ${m.cls}">${esc(m.val)}</div><div class="mi-s">${esc(m.sub)}</div></div>`).join('');

// Plays HTML
const playsArr=Array.isArray(d.plays)?d.plays:[];
const playTypeIcon={SAFE:'🛡️',AGGRESSIVE:'⚡',CONTRARIAN:'🔄'};
const playTypeCls={SAFE:'up',AGGRESSIVE:'bear',CONTRARIAN:'neut'};
const playsHTML=playsArr.length?playsArr.map((p,i)=>{
  const locked=p.type!=='SAFE';
  const inner='<div class="play-card-type '+(playTypeCls[p.type]||'neut')+'">'+(playTypeIcon[p.type]||'\u2697')+' '+esc(p.type)+'</div><div class="play-card-thesis">'+esc(p.thesis)+'</div><div class="play-card-details">'+renderBrief(p.details)+'</div>';
  return '<div class="play-card" style="animation-delay:'+i*100+'ms">'+inner+'</div>';
}).join(''):'<div class="play-text">No plays generated.</div>';

// Trap and Edge HTML
const trapHTML=d.trap?`<section class="trap rv"><div class="trap-icon">⚠</div><div class="trap-tag">MARKET TRAP</div><div class="trap-text">${renderBrief(d.trap)}</div></section>`:'';
const edgeHTML=d.edge?`<section class="edge-section rv"><div class="edge-tag">🔍 THE EDGE — WHAT OTHERS ARE MISSING</div><div class="edge-text">${renderBrief(d.edge)}</div></section>`:'';

// Alpha Telemetry (Whale/Liqs)
let alphaHTML = '';
if (d.alpha_telemetry && d.alpha_telemetry.flush_detection) {
  const at = d.alpha_telemetry;
  alphaHTML = `
  <section class="glass-card rv" style="margin-bottom:48px; border-left: 3px solid var(--blue)">
    <div class="sec-title" style="color: var(--blue)">🐋 WHALE & LIQUIDITY TELEMETRY</div>
    <div style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 12px; font-weight: 700;">
      Cumulative Leverage: <span class="neut">${esc(at.flush_detection.cumulative_leverage)}</span>
    </div>
    <div style="color: var(--ink2); line-height: 1.6; margin-bottom: 16px;">
      ${esc(at.flush_detection.analysis)}
    </div>
    <div class="mgrid" style="grid-template-columns:repeat(2,1fr)">
      <div class="mi"><div class="mi-l">Lower Margin Support</div><div class="mi-v bear">${esc(at.flush_detection.support_margin_lower)}</div></div>
      <div class="mi"><div class="mi-l">Upper Margin Support</div><div class="mi-v up">${esc(at.flush_detection.support_margin_upper)}</div></div>
    </div>
  </section>`;
}

// Autopsy Resolutions
let autopsyHTML = '';
if (d.autopsy_resolutions && d.autopsy_resolutions.length > 0) {
  const rs = d.autopsy_resolutions.map(r => `
    <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--dim);">
      <span style="display:inline-block; padding: 2px 6px; font-size: 0.8rem; font-weight: 700; border-radius: 4px; background: ${r.status==='WIN'?'var(--green-g)':r.status==='LOSS'?'var(--red-g)':'var(--dim)'}; color: ${r.status==='WIN'?'var(--green)':r.status==='LOSS'?'var(--red)':'var(--ink)'}; margin-right: 8px;">${esc(r.status)}</span>
      <span style="font-weight: 700">${esc(r.pnl_percent)}</span>
      <p style="color: var(--ink2); font-size: 0.95rem; margin-top: 4px;">${esc(r.autopsy_note)}</p>
    </div>
  `).join('');
  autopsyHTML = `
  <section class="glass-card rv" style="margin-bottom:48px; border-left: 3px solid var(--purple)">
    <div class="sec-title" style="color: var(--purple)">📝 SIGNAL AUTOPSY (RESOLUTION DESK)</div>
    ${rs}
  </section>`;
}

// Key Levels
const kl=d.key_levels||{};
const keyHTML=Object.keys(kl).length?`<section class="glass-card rv" style="margin-bottom:48px"><div class="sec-title">KEY LEVELS TO WATCH</div><div class="mgrid" style="grid-template-columns:repeat(2,1fr)">${kl.btc_support?`<div class="mi"><div class="mi-l">BTC Support</div><div class="mi-v neut">${esc(kl.btc_support)}</div><div class="mi-s">Break = bearish</div></div>`:''} ${kl.btc_resistance?`<div class="mi"><div class="mi-l">BTC Resistance</div><div class="mi-v neut">${esc(kl.btc_resistance)}</div><div class="mi-s">Break = momentum</div></div>`:''} ${kl.spx_support?`<div class="mi"><div class="mi-l">SPX Support</div><div class="mi-v neut">${esc(kl.spx_support)}</div><div class="mi-s">Pivot level</div></div>`:''} ${kl.yield_threshold?`<div class="mi"><div class="mi-l">Yield Threshold</div><div class="mi-v bear">${esc(kl.yield_threshold)}</div><div class="mi-s">Breaks calm if hit</div></div>`:''}</div></section>`:'';

// Cross Market Context
const cmBond=d.cross_market?.bond||{label:'CAUTION',desc:`10Y at ${esc(d.yieldVal||'—')}% — bond market pricing fiscal risk.`};
const cmEquity=d.cross_market?.equity||{label:'CALM',desc:`Equities holding. ${esc(d.spxChange||'')} session.`};
const cmCrypto=d.cross_market?.crypto||{label:'HEDGING',desc:`BTC at ${esc(d.btcPrice)} — hard asset demand.`};
const cmSentiment=d.cross_market?.sentiment||{label:`FEAR ${d.fearIndex}`,desc:`${d.fearLabel||'Mixed'} sentiment across retail.`};
const cmClasses=[
  {label:'Bond Market',val:cmBond.label,desc:cmBond.desc,cls:cmBond.label==='CAUTION'||cmBond.label==='RISK'?'dn':'neut',accent:'var(--red)'},
  {label:'Equity Market',val:cmEquity.label,desc:cmEquity.desc,cls:cmEquity.label==='CALM'||cmEquity.label==='BULLISH'?'up':'neut',accent:'var(--green)'},
  {label:'Crypto',val:cmCrypto.label,desc:cmCrypto.desc,cls:'neut',accent:'var(--gold)'},
  {label:'Sentiment',val:cmSentiment.label,desc:cmSentiment.desc,cls:d.fearIndex>50?'dn':'up',accent:'var(--purple)'}
];
const contextHTML=cmClasses.map((c,i)=>`<div class="ctx-card" style="--accent:${c.accent};animation-delay:${i*100}ms"><div class="ctx-l">${esc(c.label)}</div><div class="ctx-v ${c.cls}">${esc(c.val)}</div><div class="ctx-d">${esc(c.desc)}</div></div>`).join('');

// THE FINAL HTML
const html=`<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chaos Intelligence v7 — ${esc(d.headline)}</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@300;400;700&family=Barlow+Condensed:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<style>
:root{--bg:#08080c;--bg2:#0d0d12;--s0:#101016;--s1:#14141c;--s2:#1a1a24;--s3:#22222e;--s4:#2c2c3c;--ink:#f0ece4;--ink2:#b8b0a4;--muted:#5a5a6e;--dim:#28283a;--red:#e8394a;--red-g:rgba(232,57,74,.12);--green:#22d45a;--green-g:rgba(34,212,90,.1);--gold:#f5a623;--gold-g:rgba(245,166,35,.1);--blue:#4cc9f0;--purple:#9d6cf8;--font-big:'Bebas Neue',sans-serif;--font-body:'Crimson Pro',serif;--font-mono:'JetBrains Mono',monospace;--font-ui:'Barlow Condensed',sans-serif;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);padding:24px; max-width:800px; margin:0 auto; line-height: 1.6;}
.hdr-top { font-family: var(--font-big); font-size: 3rem; margin-bottom: 24px; color: var(--gold); border-bottom: 1px solid var(--s3); padding-bottom: 12px; }
.headline { font-size: 2.5rem; font-family: var(--font-ui); font-weight: 700; line-height: 1.1; margin-bottom: 24px; }
.chaos-line { font-family: var(--font-mono); font-size: 1.1rem; color: var(--gold); padding: 16px; background: var(--s0); border-left: 3px solid var(--gold); margin-bottom: 32px; }
.glass-card { background: var(--s1); border: 1px solid var(--dim); border-radius: 8px; padding: 24px; margin-bottom: 24px; }
.sec-title { font-family: var(--font-mono); font-size: 0.8rem; letter-spacing: 2px; color: var(--muted); margin-bottom: 16px; }
.mgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 16px; margin-bottom: 32px; }
.mi { background: var(--s0); padding: 12px; border-radius: 6px; }
.mi-l { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); margin-bottom: 4px; }
.mi-v { font-family: var(--font-mono); font-size: 1.2rem; font-weight: 700; }
.mi-v.up { color: var(--green); } .mi-v.dn { color: var(--red); } .mi-v.neut { color: var(--ink); }
.mi-s { font-size: 0.85rem; color: var(--ink2); margin-top: 4px; }
.ctx-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 32px; }
.ctx-card { background: var(--s0); border-top: 2px solid var(--accent); padding: 16px; }
.ctx-l { font-family: var(--font-mono); font-size: 0.75rem; color: var(--muted); margin-bottom: 8px; }
.ctx-v { font-family: var(--font-ui); font-size: 1.4rem; font-weight: 700; margin-bottom: 8px; }
.ctx-v.up { color: var(--green); } .ctx-v.dn { color: var(--red); } .ctx-v.neut { color: var(--gold); }
.ctx-d { font-size: 0.95rem; color: var(--ink2); }
.play-card { background: var(--s1); border-left: 3px solid var(--gold); padding: 20px; margin-bottom: 16px; border-radius: 0 8px 8px 0; }
.play-card-type { font-family: var(--font-mono); font-weight: 700; font-size: 0.8rem; margin-bottom: 8px; display: inline-block; padding: 4px 8px; border-radius: 4px; background: var(--s2); }
.play-card-type.up { color: var(--green); } .play-card-type.bear { color: var(--red); } .play-card-type.neut { color: var(--gold); }
.play-card-thesis { font-family: var(--font-ui); font-size: 1.5rem; font-weight: 700; margin-bottom: 12px; }
.wire { padding: 12px; border-bottom: 1px solid var(--dim); }
.wire-src { font-family: var(--font-mono); font-size: 0.7rem; color: var(--blue); margin-right: 8px; }
.wire-hl { font-size: 1.1rem; font-weight: 600; margin: 4px 0; }
.wire-body { font-size: 0.95rem; color: var(--ink2); }
.trap { background: rgba(232,57,74,0.05); border: 1px solid var(--red-g); padding: 24px; border-radius: 8px; margin-bottom: 24px; }
.trap-tag { font-family: var(--font-mono); color: var(--red); font-size: 0.8rem; margin-bottom: 12px; font-weight: 700; }
.edge-section { background: rgba(245,166,35,0.05); border: 1px solid var(--gold-g); padding: 24px; border-radius: 8px; margin-bottom: 24px; }
.edge-tag { font-family: var(--font-mono); color: var(--gold); font-size: 0.8rem; margin-bottom: 12px; font-weight: 700; }
.forces-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
.fc { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 20px; background: var(--s0); font-family: var(--font-mono); font-size: 0.8rem; }
.fc.on { border: 1px solid var(--gold); color: var(--gold); }
.fc.off { opacity: 0.5; }
.fc-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--dim); }
.fc.on .fc-dot { background: var(--gold); box-shadow: 0 0 8px var(--gold); }
</style>
</head>
<body>
  <div class="hdr-top">CHAOS INTELLIGENCE <span>v7</span></div>
  <div class="headline">${esc(d.headline)}</div>
  <div class="chaos-line">"${esc(d.chaos_line)}"</div>
  
  <div class="sec-title">MACRO DASHBOARD</div>
  <div class="mgrid">${macroHTML}</div>
  
  <div class="ctx-grid">${contextHTML}</div>
  
  ${alphaHTML}
  ${autopsyHTML}
  
  <div class="glass-card">
    <div class="sec-title">THE ANALYST DESK</div>
    <div style="font-size: 1.15rem; line-height: 1.7; color: var(--ink)">${renderBrief(d.analyst)}</div>
  </div>
  
  <div class="sec-title">ACTIVE FORCES</div>
  <div class="forces-wrap">${forcesHTML}</div>
  
  ${trapHTML}
  ${edgeHTML}
  
  <div class="sec-title">ACTIONABLE PLAYS</div>
  <div>${playsHTML}</div>
  
  ${keyHTML}
  
  <div class="glass-card">
    <div class="sec-title">GEOPOLITICAL WIRES</div>
    <div>${wiresHTML}</div>
  </div>
  
  <div style="text-align: center; margin-top: 60px; padding: 20px; font-family: var(--font-mono); font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--s3);">
    Generated at ${timeStr} | Chaos Intelligence v7<br>
    Powered by Llama 3.1, Gemini Flash, and Claude 3.5 Sonnet
  </div>
</body>
</html>`;

return [{ json: { ...d, html: html } }];
"""

# Create the new node
html_builder_node = {
    "parameters": {"jsCode": html_builder_code.strip()},
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [800, 400],
    "id": "html-builder-v7",
    "name": "HTML Builder v7"
}

# Add node to workflow
wf['nodes'].append(html_builder_node)

# Update connections: Merge All Brains -> HTML Builder v7 -> GitHub Deploy Prep
conns = wf['connections']

# Remove Merge -> GitHub Deploy Prep
if 'Merge All Brains' in conns:
    conns['Merge All Brains']['main'][0] = [
        c for c in conns['Merge All Brains']['main'][0] 
        if c['node'] != 'GitHub Deploy Prep'
    ]

# Add Merge -> HTML Builder
conns['Merge All Brains']['main'][0].append({
    "node": "HTML Builder v7",
    "type": "main",
    "index": 0
})

# Add HTML Builder -> GitHub Deploy Prep
conns['HTML Builder v7'] = {
    "main": [
        [{
            "node": "GitHub Deploy Prep",
            "type": "main",
            "index": 0
        }]
    ]
}

with open('chaos_v7_complete.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("Added HTML Builder v7 node successfully!")
