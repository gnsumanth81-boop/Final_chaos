import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# The new GitHub Deploy Prep node - outputs JSON for api/latest.json instead of HTML
new_github_prep_code = """const d = $input.first().json;
const cfg = $('\\u2699\\ufe0f CONFIG').first().json;

// Build the latest.json structure that the static UI reads
const latestJson = {
  market: {
    fearIndex: d.fearIndex,
    fearLabel: d.fearLabel,
    fearDelta: d.fearDelta,
    btcPrice: d.btcPrice,
    btcChange: d.btcChange,
    btcVolume: d.btcVolume,
    btcHigh: d.btcHigh,
    btcLow: d.btcLow,
    ethPrice: d.ethPrice,
    ethChange: d.ethChange,
    vixVal: d.vixVal,
    yieldVal: d.yieldVal,
    yieldPrev: d.yieldPrev,
    dxyVal: d.dxyVal,
    spxVal: d.spxVal,
    spxChange: d.spxChange,
    marketTitle: d.marketTitle,
    marketOdds: d.marketOdds,
    marketVolume: d.marketVolume,
    marketLink: d.marketLink,
    session: d.sessionLabel,
    newsText: d.newsText,
    btcDominance: d.btcDominance,
    totalMarketCap: d.totalMarketCap,
    stablecoinPct: d.stablecoinPct,
    wsbSentiment: d.wsbSentiment,
    wsbTopTickers: d.wsbTopTickers,
    recessionProb: d.recessionProb,
    goldPrice: d.goldPrice || 'N/A',
    label: d.sessionLabel + ' SESSION'
  },
  brief: {
    headline: d.headline,
    dateline: d.dateline,
    signal: d.signal,
    confidence: d.confidence,
    eli5: d.eli5,
    analyst: d.analyst,
    quant: d.quant,
    chaos_line: d.chaos_line,
    plays: d.plays || [],
    trap: d.trap,
    edge: d.edge,
    time_sensitivity: d.time_sensitivity,
    forces: d.forces || [],
    active_regime: d.active_regime,
    cross_market: d.cross_market || {},
    news_wires: d.news_wires || [],
    key_levels: d.key_levels || {},
    weekly_catalyst: d.weekly_catalyst || '',
    agent_consensus: d.agent_consensus || { debate_required: false, resolution: '' },
    generated_at: d.generated_at
  },
  agents: {
    fundamental: (d.alpha_telemetry && Object.keys(d.alpha_telemetry).length > 0) ? {
      bias: d.signal || 'NEUTRAL',
      thesis: d.alpha_telemetry.flush_detection?.analysis || 'Whale data analysis complete.'
    } : { bias: 'NEUTRAL', thesis: 'Awaiting whale data...' },
    technical: {
      bias: parseFloat(d.btcChange || 0) > 0 ? 'BULLISH' : parseFloat(d.btcChange || 0) < 0 ? 'BEARISH' : 'NEUTRAL',
      thesis: 'BTC ' + (parseFloat(d.btcChange || 0) >= 0 ? 'positive' : 'negative') + ' momentum. VIX at ' + (d.vixVal || 'N/A') + '.'
    },
    sentiment: {
      bias: d.fearIndex > 60 ? 'BULLISH' : d.fearIndex < 30 ? 'BEARISH' : 'NEUTRAL',
      thesis: 'Fear & Greed at ' + d.fearIndex + ' (' + (d.fearLabel || 'Neutral') + '). WSB: ' + (d.wsbSentiment || 'N/A') + '.'
    }
  },
  signal: {
    signal_hash: 'CI-' + Date.now().toString(36).toUpperCase() + '-' + (d.signal || 'N')[0],
    timestamp: d.generated_at
  }
};

const base64Content = Buffer.from(JSON.stringify(latestJson, null, 2), 'utf-8').toString('base64');

return [{
  json: {
    latest_json: latestJson,
    latest_base64: base64Content,
    repo_owner: cfg.GITHUB_USERNAME || 'gnsumanth81-boop',
    repo_name: cfg.GITHUB_REPO || 'Final_chaos',
    commit_message: 'Chaos Intelligence v7 — ' + (d.headline || 'Auto-deploy') + ' | ' + new Date().toISOString().substring(0, 16)
  }
}];"""

# New GitHub Get SHA node for api/latest.json
new_get_sha_params = {
    "method": "GET",
    "url": "={{ 'https://api.github.com/repos/' + $json.repo_owner + '/' + $json.repo_name + '/contents/api/latest.json' }}",
    "sendHeaders": True,
    "headerParameters": {"parameters": [
        {"name": "Authorization", "value": "=token {{ $('⚙️ CONFIG').first().json.GITHUB_PAT }}"},
        {"name": "Accept", "value": "application/vnd.github.v3+json"}
    ]},
    "options": {"timeout": 10000}
}

# New GitHub Push node for api/latest.json
new_push_params = {
    "method": "PUT",
    "url": "={{ 'https://api.github.com/repos/' + $('GitHub Deploy Prep').first().json.repo_owner + '/' + $('GitHub Deploy Prep').first().json.repo_name + '/contents/api/latest.json' }}",
    "sendHeaders": True,
    "headerParameters": {"parameters": [
        {"name": "Authorization", "value": "=token {{ $('⚙️ CONFIG').first().json.GITHUB_PAT }}"},
        {"name": "Accept", "value": "application/vnd.github.v3+json"},
        {"name": "Content-Type", "value": "application/json"}
    ]},
    "sendBody": True,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify({ message: $('GitHub Deploy Prep').first().json.commit_message, content: $('GitHub Deploy Prep').first().json.latest_base64, sha: $json.sha || undefined }) }}",
    "options": {"timeout": 15000}
}

# Update nodes
for node in wf['nodes']:
    if node['name'] == 'GitHub Deploy Prep':
        node['parameters']['jsCode'] = new_github_prep_code
        print("Updated: GitHub Deploy Prep -> now outputs api/latest.json")
    if node['name'] == 'GitHub Get SHA':
        node['parameters'] = new_get_sha_params
        print("Updated: GitHub Get SHA -> points to api/latest.json")
    if node['name'] == 'GitHub Push to Pages':
        node['parameters'] = new_push_params
        print("Updated: GitHub Push -> writes to api/latest.json")
    # Remove HTML Builder - it's no longer needed (UI is static now)
    if node['name'] == 'HTML Builder v7':
        node['parameters']['jsCode'] = """// HTML Builder is no longer needed.
// The UI is now a static index.html on GitHub.
// n8n only updates api/latest.json with live data.
return [{ json: $input.first().json }];"""
        print("Disabled: HTML Builder v7 (now a passthrough)")

with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("\nWorkflow updated! n8n now pushes api/latest.json to GitHub.")
print("The static index.html (your masterpiece UI) is already live and never needs to change.")
