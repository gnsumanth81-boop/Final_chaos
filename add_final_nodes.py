import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load current workflow
with open('chaos_v7_complete.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# ================================================================
# NODE 1: Chaos Pre-Processor v5 (the massive data merger)
# ================================================================
preprocessor_code = r"""
function safeGet(nodeId, path) {
  try {
    const parts = path.split('.');
    let val = $(nodeId).first().json;
    for (const p of parts) val = val?.[p];
    return val;
  } catch (e) { return null; }
}

// Fear & Greed
const fearData = safeGet('FearGreedAPI', 'data') || [];
const fearToday = fearData[0] || {};
const fearYest = fearData[1] || {};
const fearIndex = parseInt(fearToday.value || 50);
const fearLabel = fearToday.classification || 'Neutral';
const fearYestVal = parseInt(fearYest.value || fearIndex);
const fearDelta = fearIndex - fearYestVal;

// BTC
let btcPrice = 'N/A', btcChange = '0.00', btcVolume = 'N/A', btcHigh = 'N/A', btcLow = 'N/A';
try {
  const b = $('BinanceBTC').first().json;
  btcPrice = '$' + parseFloat(b.lastPrice || 0).toLocaleString('en-US', { maximumFractionDigits: 0 });
  btcChange = parseFloat(b.priceChangePercent || 0).toFixed(2);
  btcVolume = '$' + (parseFloat(b.quoteVolume || 0) / 1e9).toFixed(1) + 'B';
  btcHigh = '$' + parseFloat(b.highPrice || 0).toLocaleString('en-US', { maximumFractionDigits: 0 });
  btcLow = '$' + parseFloat(b.lowPrice || 0).toLocaleString('en-US', { maximumFractionDigits: 0 });
} catch (e) {}

// ETH
let ethPrice = 'N/A', ethChange = '0.00';
try {
  const e = $('BinanceETH').first().json;
  ethPrice = '$' + parseFloat(e.lastPrice || 0).toLocaleString('en-US', { maximumFractionDigits: 0 });
  ethChange = parseFloat(e.priceChangePercent || 0).toFixed(2);
} catch (e) {}

// VIX
let vixVal = 'N/A';
try {
  const v = $('VIX Index').first().json;
  const closes = v.chart?.result?.[0]?.indicators?.quote?.[0]?.close || [];
  vixVal = closes[closes.length - 1]?.toFixed(2) || 'N/A';
} catch (e) {}

// 10Y Treasury
let yieldVal = 'N/A', yieldPrev = 'N/A';
try {
  const t = $('10Y Treasury').first().json;
  const closes = t.chart?.result?.[0]?.indicators?.quote?.[0]?.close || [];
  yieldVal = closes[closes.length - 1]?.toFixed(3) || 'N/A';
  yieldPrev = closes[closes.length - 2]?.toFixed(3) || 'N/A';
} catch (e) {}

// DXY
let dxyVal = 'N/A';
try {
  const d = $('DXY Dollar').first().json;
  const closes = d.chart?.result?.[0]?.indicators?.quote?.[0]?.close || [];
  dxyVal = closes[closes.length - 1]?.toFixed(2) || 'N/A';
} catch (e) {}

// SPX
let spxVal = 'N/A', spxChange = 'N/A';
try {
  const s = $('S&P 500').first().json;
  const closes = s.chart?.result?.[0]?.indicators?.quote?.[0]?.close || [];
  const validCloses = closes.filter(c => c != null && isFinite(c) && c > 0);
  if (validCloses.length >= 1) {
    spxVal = validCloses[validCloses.length - 1].toLocaleString('en-US', { maximumFractionDigits: 0 });
  }
  if (validCloses.length >= 2) {
    const curr = validCloses[validCloses.length - 1];
    const prev = validCloses[validCloses.length - 2];
    if (prev > 0 && isFinite(prev) && isFinite(curr)) {
      const chg = ((curr - prev) / prev) * 100;
      if (Math.abs(chg) < 20) {
        spxChange = (chg >= 0 ? '+' : '') + chg.toFixed(2) + '%';
      }
    }
  }
} catch (e) {}

// Polymarket
let mkt = {}; try { mkt = $('Limit to Top 1').first().json || {}; } catch(e) {}
const marketTitle = mkt.Title || 'Unknown';
const marketOdds = mkt.Odds || '50.0';
const marketVolume = mkt.Volume || '$0';
const marketLink = mkt.Link || 'https://polymarket.com';

// News
let articles = []; try { articles = $('ContextNews').first().json?.articles || []; } catch(e) {}
const newsText = articles.slice(0, 10)
  .map((a, i) => `${i + 1}. ${a.title || 'Untitled'} [${a.source?.name || 'Wire'}]`)
  .join('\n');

// CoinGecko
let btcDominance = 'N/A', totalMarketCap = 'N/A', stablecoinPct = 'N/A';
try {
  const cg = $('CoinGecko').first().json?.data;
  if (cg) {
    btcDominance = (cg.market_cap_percentage?.btc || 0).toFixed(1) + '%';
    totalMarketCap = '$' + (cg.total_market_cap?.usd / 1e12).toFixed(2) + 'T';
    stablecoinPct = cg.market_cap_change_percentage_24h_usd
      ? (cg.market_cap_change_percentage_24h_usd > 0 ? 'Inflows' : 'Outflows')
      : 'N/A';
  }
} catch (e) {}

// Reddit WSB
let wsbSentiment = 'N/A', wsbTopTickers = 'No data';
try {
  const posts = $('Reddit WSB').first().json?.data?.children || [];
  const titles = posts.map(p => p.data?.title || '').join(' ');
  const tickerRegex = /\$([A-Z]{2,5})\b/g;
  const tickers = [];
  let match;
  while ((match = tickerRegex.exec(titles)) !== null) tickers.push(match[1]);
  const counts = {};
  tickers.forEach(t => counts[t] = (counts[t] || 0) + 1);
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5);
  wsbTopTickers = sorted.length ? sorted.map(([t, c]) => `${t}(${c})`).join(', ') : 'No ticker mentions';
  const bullWords = (titles.match(/moon|call|buy|long|bull|rip|squeeze|rocket/gi) || []).length;
  const bearWords = (titles.match(/put|short|bear|crash|dump|sell|drill|rug/gi) || []).length;
  wsbSentiment = bullWords > bearWords + 2 ? 'BULLISH' : bearWords > bullWords + 2 ? 'BEARISH' : 'MIXED';
} catch (e) {}

// FRED
let recessionProb = 'N/A';
try {
  const fred = $('FRED Recession').first().json;
  const obs = fred?.observations || [];
  if (obs.length > 0) recessionProb = parseFloat(obs[0].value).toFixed(1) + '%';
} catch (e) {}

// Session
const hour = new Date().getUTCHours();
const sessionLabel = hour < 12 ? 'MORNING' : hour < 17 ? 'AFTERNOON' : 'EVENING';

// THE PROMPT
const promptText = `ROLE: You are CHAOS INTELLIGENCE - a world-class Macro Hedge Fund Analyst.
TONE: Sharp, cynical, authoritative, zero fluff.

TASK:
1. NARRATIVE ARBITRAGE - Find where retail consensus is wrong.
2. REGIME DETECTION - Risk-On / Risk-Off / Liquidity Trap.
3. FORCE ANALYSIS - Rate each of the 9 Forces.
4. SIGNAL + PLAYS - Generate 3 Plays with conviction %.

OUTPUT ONLY VALID JSON (no markdown).

INPUT DATA:
- Session: ${sessionLabel}
- Fear & Greed: ${fearIndex} (${fearLabel}) | Yesterday: ${fearYestVal} | Delta: ${fearDelta > 0 ? '+' : ''}${fearDelta}
- Bitcoin: ${btcPrice} (${btcChange}% 24h) | Vol: ${btcVolume} | High: ${btcHigh} | Low: ${btcLow}
- Ethereum: ${ethPrice} (${ethChange}% 24h)
- VIX: ${vixVal}
- 10Y Treasury: ${yieldVal}% (prev: ${yieldPrev}%)
- DXY: ${dxyVal}
- S&P 500: ${spxVal} (${spxChange})
- BTC Dominance: ${btcDominance} | Total Crypto MCap: ${totalMarketCap} | Stablecoin Flow: ${stablecoinPct}
- Reddit/WSB Sentiment: ${wsbSentiment} | Top Tickers: ${wsbTopTickers}
- US Recession Probability: ${recessionProb}
- Top Prediction Market: "${marketTitle}" - ${marketOdds}% odds - ${marketVolume} volume
- Headlines:\n${newsText || 'No headlines available.'}

OUTPUT JSON FORMAT:
{
  "headline": "5-8 words punchy headline",
  "dateline": "Most relevant city",
  "eli5": "3-4 sentences for a smart 16-year-old. Use \\n\\n between paragraphs.",
  "analyst": "5-6 sentences for a finance professional. Use \\n\\n.",
  "quant": "5-6 sentences for a trader. Use \\n\\n.",
  "chaos_line": "ONE sentence, 12-22 words. Poetic. Devastating. Screenshot-worthy.",
  "plays": [
    { "type": "SAFE", "thesis": "Low risk setup", "details": "Asset + direction + level + catalyst" },
    { "type": "AGGRESSIVE", "thesis": "High conviction bet", "details": "Clear directional bet" },
    { "type": "CONTRARIAN", "thesis": "Against the crowd", "details": "Why consensus is wrong" }
  ],
  "trap": "2-3 sentences. Who is positioned WRONG.",
  "edge": "1-2 sentences. What most people are NOT watching.",
  "time_sensitivity": "IMMEDIATE or TODAY or THIS WEEK",
  "forces": ["2-4 active forces from: MONEY, TECH, ENERGY, POLITICS, WAR, DEBT, JOBS, FOOD, PEOPLE"],
  "confidence": 74,
  "signal": "BULLISH or BEARISH or NEUTRAL or VOLATILE",
  "active_regime": "RISK-ON or RISK-OFF or LIQUIDITY TRAP",
  "macro_dashboard": {
    "yield_10y": "${yieldVal}%", "yield_delta": "change", "dxy": "${dxyVal}", "vix": "${vixVal}",
    "spx": "${spxVal}", "spx_delta": "${spxChange}", "btc_dominance": "${btcDominance}",
    "recession_prob": "${recessionProb}"
  },
  "cross_market": {
    "bond": { "label": "CAUTION/CALM/RISK", "desc": "1 sentence" },
    "equity": { "label": "BULLISH/CALM/STRESSED", "desc": "1 sentence" },
    "crypto": { "label": "RISK-ON/HEDGING/FEAR", "desc": "1 sentence" },
    "sentiment": { "label": "FEAR X/GREED X", "desc": "1 sentence" }
  },
  "news_wires": [
    { "source": "SOURCE", "title": "headline", "impact": "2-3 sentences", "forces": ["FORCE1"] }
  ],
  "key_levels": {
    "btc_support": "key BTC support", "btc_resistance": "key BTC resistance",
    "spx_support": "key SPX support", "yield_threshold": "10Y yield level"
  },
  "weekly_catalyst": "Single most important scheduled event"
}`;

return [{
  json: {
    promptText,
    fearIndex, fearLabel, fearDelta,
    btcPrice, btcChange, btcVolume, btcHigh, btcLow,
    ethPrice, ethChange,
    vixVal, yieldVal, yieldPrev, dxyVal, spxVal, spxChange,
    marketTitle, marketOdds, marketVolume, marketLink,
    sessionLabel, newsText,
    btcDominance, totalMarketCap, stablecoinPct,
    wsbSentiment, wsbTopTickers,
    recessionProb
  }
}];
"""

# ================================================================
# NODE 2: OpenRouter Supervisor (sends prompt to AI)
# ================================================================
supervisor_code = r"""
const pp = $input.first().json;
const cfg = $('⚙️ CONFIG').first().json;

return [{
  json: {
    model: 'google/gemini-2.5-flash',
    messages: [{ role: 'user', content: pp.promptText }],
    temperature: 0.6,
    response_format: { type: 'json_object' }
  }
}];
"""

# ================================================================
# NODE 3: Parse Supervisor Response
# ================================================================
parse_supervisor_code = r"""
const raw = $input.first().json;
let parsed = {};
try {
  const content = raw.choices?.[0]?.message?.content || '{}';
  parsed = JSON.parse(content);
} catch(e) {
  parsed = { headline: 'Parse Error', signal: 'NEUTRAL', confidence: 50 };
}
return [{ json: parsed }];
"""

# ================================================================
# NODE 4: Merge All Brains
# ================================================================
merge_code = r"""
// Merge outputs from Supervisor, Alpha, Autopsy, and Geo brains
function safeGet(nodeName) {
  try { return $(nodeName).first().json || {}; }
  catch(e) { return {}; }
}

const pp = safeGet('Chaos Pre-Processor v5');
const sup = safeGet('Parse Supervisor Response');

// Alpha brain
let alphaData = {};
try {
  const alphaRaw = safeGet('🐋 OpenRouter (Alpha)');
  const alphaContent = alphaRaw.choices?.[0]?.message?.content || '{}';
  alphaData = JSON.parse(alphaContent);
} catch(e) {}

// Autopsy brain
let autopsyData = {};
try {
  const autopsyRaw = safeGet('📝 OpenRouter (Autopsy)');
  if (!autopsyRaw.skip) {
    const autopsyContent = autopsyRaw.choices?.[0]?.message?.content || '{}';
    autopsyData = JSON.parse(autopsyContent);
  }
} catch(e) {}

// Geo brain
let geoData = {};
try {
  const geoRaw = safeGet('🌍 OpenRouter (Geo)');
  if (!geoRaw.skip) {
    const geoContent = geoRaw.choices?.[0]?.message?.content || '{}';
    geoData = JSON.parse(geoContent);
  }
} catch(e) {}

// Build cross-market from live data
const yieldVal = pp.yieldVal || 'N/A';
const spxChange = pp.spxChange || '';
const btcPrice = pp.btcPrice || '$0';
const fearIdx = parseInt(pp.fearIndex) || 50;

const crossMarket = {
  bond: {
    label: parseFloat(yieldVal) > 4.5 ? 'RISK' : parseFloat(yieldVal) > 4.0 ? 'CAUTION' : 'CALM',
    desc: '10Y at ' + yieldVal + '% — ' + (parseFloat(yieldVal) > 4.5 ? 'bond market pricing fiscal risk.' : 'yields within normal range.')
  },
  equity: {
    label: spxChange.startsWith('+') ? 'BULLISH' : spxChange.startsWith('-') ? 'CAUTION' : 'CALM',
    desc: 'S&P 500 ' + (spxChange || 'flat') + ' session.'
  },
  crypto: {
    label: parseFloat(pp.btcChange || 0) > 2 ? 'RALLY' : parseFloat(pp.btcChange || 0) < -2 ? 'SELLOFF' : 'HEDGING',
    desc: 'BTC at ' + btcPrice + ' — ' + (parseFloat(pp.btcChange || 0) >= 0 ? 'positive momentum.' : 'under pressure.')
  },
  sentiment: {
    label: 'FEAR ' + fearIdx,
    desc: (pp.fearLabel || 'Mixed') + ' sentiment across retail.'
  }
};

// Merge news_wires: prefer Geo brain output over Supervisor
const newsWires = (geoData.intel_wires || sup.news_wires || []).map(w => ({
  source: w.source || 'WIRE',
  title: w.title || '',
  impact: w.impact || '',
  forces: w.forces || []
}));

return [{ json: {
  ...pp,
  headline: sup.headline || 'Market Update',
  dateline: sup.dateline || 'NYC',
  signal: sup.signal || 'NEUTRAL',
  confidence: sup.confidence || 65,
  eli5: sup.eli5 || 'Analysis underway.',
  analyst: sup.analyst || 'Analysis underway.',
  quant: sup.quant || 'Analysis underway.',
  chaos_line: sup.chaos_line || 'The market speaks in contradictions.',
  plays: Array.isArray(sup.plays) ? sup.plays : [],
  trap: sup.trap || '',
  edge: sup.edge || '',
  time_sensitivity: sup.time_sensitivity || 'THIS WEEK',
  forces: Array.isArray(sup.forces) ? sup.forces : ['MONEY'],
  active_regime: sup.active_regime || 'TRANSITION',
  cross_market: crossMarket,
  macro_dashboard: sup.macro_dashboard || {},
  news_wires: newsWires,
  key_levels: sup.key_levels || {},
  weekly_catalyst: sup.weekly_catalyst || '',
  alpha_telemetry: alphaData,
  autopsy_resolutions: autopsyData.resolutions || [],
  generated_at: new Date().toISOString()
}}];
"""

# ================================================================
# NODE 5: GitHub Deploy (pushes index.html to GitHub Pages)
# ================================================================
github_deploy_code = r"""
// GITHUB DEPLOY NODE
// Pushes the generated HTML to your GitHub Pages repository
const cfg = $('⚙️ CONFIG').first().json;
const htmlContent = $input.first().json.html || '<h1>No content generated</h1>';

// Base64 encode the HTML for GitHub API
const base64Content = Buffer.from(htmlContent, 'utf-8').toString('base64');

// First, try to get the current file SHA (needed for updates)
return [{
  json: {
    html_base64: base64Content,
    repo_owner: cfg.GITHUB_USERNAME || 'YOUR_GITHUB_USERNAME',
    repo_name: cfg.GITHUB_REPO || 'chaos-terminal',
    file_path: 'index.html',
    commit_message: 'Chaos Intelligence v7 — Auto-deploy ' + new Date().toISOString().substring(0, 16)
  }
}];
"""

# ================================================================
# ADD NODES
# ================================================================
new_nodes = [
    {
        "parameters": {"jsCode": preprocessor_code.strip()},
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [-200, 400],
        "id": "preprocessor-v5",
        "name": "Chaos Pre-Processor v5",
        "continueOnFail": True
    },
    {
        "parameters": {"jsCode": supervisor_code.strip()},
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [0, 400],
        "id": "supervisor-prompt",
        "name": "Supervisor Prompt"
    },
    {
        "parameters": {
            "method": "POST",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "sendHeaders": True,
            "headerParameters": {"parameters": [
                {"name": "Authorization", "value": "=Bearer {{ $('⚙️ CONFIG').first().json.OPENROUTER_KEY }}"},
                {"name": "Content-Type", "value": "application/json"}
            ]},
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify({ model: $json.model, messages: $json.messages, temperature: $json.temperature, response_format: $json.response_format }) }}",
            "options": {"timeout": 60000}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [200, 400],
        "id": "supervisor-openrouter",
        "name": "OpenRouter (Supervisor)",
        "continueOnFail": True
    },
    {
        "parameters": {"jsCode": parse_supervisor_code.strip()},
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [400, 400],
        "id": "parse-supervisor",
        "name": "Parse Supervisor Response"
    },
    {
        "parameters": {"jsCode": merge_code.strip()},
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [600, 400],
        "id": "merge-all-brains",
        "name": "Merge All Brains",
        "continueOnFail": True
    },
    {
        "parameters": {"jsCode": github_deploy_code.strip()},
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1000, 400],
        "id": "github-deploy-prep",
        "name": "GitHub Deploy Prep"
    },
    # GitHub API: Get current file SHA
    {
        "parameters": {
            "method": "GET",
            "url": "={{ 'https://api.github.com/repos/' + $json.repo_owner + '/' + $json.repo_name + '/contents/' + $json.file_path }}",
            "sendHeaders": True,
            "headerParameters": {"parameters": [
                {"name": "Authorization", "value": "=token {{ $('⚙️ CONFIG').first().json.GITHUB_PAT }}"},
                {"name": "Accept", "value": "application/vnd.github.v3+json"}
            ]},
            "options": {"timeout": 10000}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [1200, 400],
        "id": "github-get-sha",
        "name": "GitHub Get SHA",
        "continueOnFail": True
    },
    # GitHub API: Push/Update file
    {
        "parameters": {
            "method": "PUT",
            "url": "={{ 'https://api.github.com/repos/' + $('GitHub Deploy Prep').first().json.repo_owner + '/' + $('GitHub Deploy Prep').first().json.repo_name + '/contents/' + $('GitHub Deploy Prep').first().json.file_path }}",
            "sendHeaders": True,
            "headerParameters": {"parameters": [
                {"name": "Authorization", "value": "=token {{ $('⚙️ CONFIG').first().json.GITHUB_PAT }}"},
                {"name": "Accept", "value": "application/vnd.github.v3+json"},
                {"name": "Content-Type", "value": "application/json"}
            ]},
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify({ message: $('GitHub Deploy Prep').first().json.commit_message, content: $('GitHub Deploy Prep').first().json.html_base64, sha: $json.sha || undefined }) }}",
            "options": {"timeout": 15000}
        },
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.3,
        "position": [1400, 400],
        "id": "github-push",
        "name": "GitHub Push to Pages",
        "continueOnFail": True
    }
]

wf['nodes'].extend(new_nodes)

# ================================================================
# ADD CONNECTIONS
# ================================================================
conns = wf['connections']

def add_conn(source, target, idx=0):
    if source not in conns:
        conns[source] = {"main": [[]]}
    if 'main' not in conns[source]:
        conns[source]['main'] = [[]]
    # Check if connection already exists
    existing = conns[source]['main'][0]
    for c in existing:
        if c['node'] == target:
            return  # Skip duplicate
    existing.append({"node": target, "type": "main", "index": idx})

# Pre-Processor -> Supervisor -> OpenRouter -> Parse -> Merge
add_conn("Chaos Pre-Processor v5", "Supervisor Prompt")
add_conn("Supervisor Prompt", "OpenRouter (Supervisor)")
add_conn("OpenRouter (Supervisor)", "Parse Supervisor Response")
add_conn("Parse Supervisor Response", "Merge All Brains")

# All 3 brain outputs also feed into Merge
add_conn("🐋 OpenRouter (Alpha)", "Merge All Brains")
add_conn("📝 OpenRouter (Autopsy)", "Merge All Brains")
add_conn("🌍 OpenRouter (Geo)", "Merge All Brains")

# Merge -> GitHub Deploy
add_conn("Merge All Brains", "GitHub Deploy Prep")
add_conn("GitHub Deploy Prep", "GitHub Get SHA")
add_conn("GitHub Get SHA", "GitHub Push to Pages")

# Remove old Parse+Validate connections if they exist
if "🐋 OpenRouter (Alpha)" in conns:
    conns["🐋 OpenRouter (Alpha)"]["main"][0] = [c for c in conns["🐋 OpenRouter (Alpha)"]["main"][0] if c["node"] != "Parse + Validate Output"]
if "📝 OpenRouter (Autopsy)" in conns:
    conns["📝 OpenRouter (Autopsy)"]["main"][0] = [c for c in conns["📝 OpenRouter (Autopsy)"]["main"][0] if c["node"] != "Parse + Validate Output"]
if "🌍 OpenRouter (Geo)" in conns:
    conns["🌍 OpenRouter (Geo)"]["main"][0] = [c for c in conns["🌍 OpenRouter (Geo)"]["main"][0] if c["node"] != "Parse + Validate Output"]

# Update CONFIG node to include new keys
for node in wf['nodes']:
    if node['name'] == '⚙️ CONFIG':
        node['parameters']['jsCode'] = """// ⚙️ CHAOS INTELLIGENCE v7 — CONFIG
// ADD YOUR API KEYS HERE
return [{ json: {
  OPENROUTER_KEY: 'YOUR_OPENROUTER_KEY_HERE',
  NEWSAPI_KEY: 'YOUR_NEWSAPI_KEY_HERE',
  FRED_KEY: 'YOUR_FRED_KEY_HERE',
  GITHUB_USERNAME: 'YOUR_GITHUB_USERNAME',
  GITHUB_REPO: 'chaos-terminal',
  GITHUB_PAT: 'YOUR_GITHUB_PERSONAL_ACCESS_TOKEN'
}}];"""
        break

# Save
with open('chaos_v7_complete.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

node_count = len(wf['nodes'])
conn_count = sum(len(v.get('main',[[]])[0]) for v in conns.values())
print("="*60)
print("CHAOS INTELLIGENCE v7 - FINAL COMPLETE WORKFLOW")
print("="*60)
print(f"Total Nodes: {node_count}")
print(f"Total Connections: {conn_count}")
print("")
print("PIPELINE:")
print("  Schedule Trigger")
print("  -> CONFIG (keys)")
print("  -> 15 Data Sources (Binance, Yahoo, News, Reddit, FRED...)")
print("  -> Chaos Pre-Processor v5 (merge all data)")
print("  -> Supervisor Prompt -> OpenRouter (Gemini Flash)")
print("  -> Parse Supervisor Response")
print("  -> Merge All Brains")
print("     + Alpha Brain (Whale/Liquidation)")
print("     + Autopsy Brain (Signal Resolution)")
print("     + Geo Brain (Macro Narrative)")
print("  -> GitHub Deploy Prep")
print("  -> GitHub Get SHA")
print("  -> GitHub Push to Pages")
print("")
print("File: chaos_v7_complete.json")
print("="*60)
