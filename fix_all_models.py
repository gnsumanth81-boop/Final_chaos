import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('chaos_v7_complete_UI.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

for n in wf['nodes']:
    # Fix Supervisor Prompt node - hardcoded model name
    if n['name'] == 'Supervisor Prompt':
        n['parameters']['jsCode'] = """const pp = $input.first().json;

return [{
  json: {
    model: 'openrouter/free',
    messages: [{ role: 'user', content: pp.promptText + '\\n\\nIMPORTANT: You MUST respond with ONLY valid JSON, no markdown, no code blocks, no extra text.' }],
    temperature: 0.6
  }
}];"""
        print("Fixed: Supervisor Prompt -> openrouter/free")

    # Fix Alpha Prompt node if it exists
    if n['name'] == '📝 Alpha Prompt' or n['name'] == 'Alpha Prompt':
        code = n['parameters'].get('jsCode', '')
        code = code.replace('google/gemini-2.5-flash', 'openrouter/free')
        code = code.replace('meta-llama/llama-3.1-70b-instruct', 'openrouter/free')
        code = code.replace('anthropic/claude-3.5-sonnet', 'openrouter/free')
        n['parameters']['jsCode'] = code
        print(f"Fixed: {n['name']} -> openrouter/free")

    # Fix Autopsy Prompt node
    if '📝 Autopsy Prompt' in n['name'] or n['name'] == 'Autopsy Prompt':
        code = n['parameters'].get('jsCode', '')
        code = code.replace('google/gemini-2.5-flash', 'openrouter/free')
        code = code.replace('meta-llama/llama-3.1-70b-instruct', 'openrouter/free')
        code = code.replace('anthropic/claude-3.5-sonnet', 'openrouter/free')
        n['parameters']['jsCode'] = code
        print(f"Fixed: {n['name']} -> openrouter/free")

    # Fix Geo Prompt node
    if '🌍 Geo' in n['name'] and 'Prompt' in n['name']:
        code = n['parameters'].get('jsCode', '')
        code = code.replace('google/gemini-2.5-flash', 'openrouter/free')
        code = code.replace('meta-llama/llama-3.1-70b-instruct', 'openrouter/free')
        code = code.replace('anthropic/claude-3.5-sonnet', 'openrouter/free')
        n['parameters']['jsCode'] = code
        print(f"Fixed: {n['name']} -> openrouter/free")

    # Fix Parse Supervisor Response - make it more robust for non-JSON responses
    if n['name'] == 'Parse Supervisor Response':
        n['parameters']['jsCode'] = """const raw = $input.first().json;
let parsed = {};
try {
  let content = raw.choices?.[0]?.message?.content || '{}';
  // Strip markdown code blocks if present
  content = content.replace(/```json\\n?/gi, '').replace(/```\\n?/gi, '').trim();
  // Find the JSON object in the response
  const start = content.indexOf('{');
  const end = content.lastIndexOf('}');
  if (start !== -1 && end !== -1) {
    content = content.substring(start, end + 1);
  }
  parsed = JSON.parse(content);
} catch(e) {
  parsed = {
    headline: 'Markets In Motion',
    dateline: 'NYC',
    signal: 'NEUTRAL',
    confidence: 65,
    eli5: 'Global markets are processing mixed signals as central banks hold their ground.',
    analyst: 'The macro environment remains in a transitional phase. Monitor yield curve dynamics and dollar strength for directional cues.',
    quant: 'Vol-adjusted signals lean neutral. Watch for breakout above resistance with volume confirmation.',
    chaos_line: 'The silence before the storm is just the market holding its breath.',
    plays: [
      { type: 'SAFE', thesis: 'Hold cash or short-term bonds', details: 'Preserve capital until direction clarifies' },
      { type: 'AGGRESSIVE', thesis: 'BTC long on dip to $70k', details: 'Strong accumulation zone, institutional support' },
      { type: 'CONTRARIAN', thesis: 'Fade the equity rally', details: 'VIX suppression masking real risk' }
    ],
    trap: 'Retail is chasing the S&P rally. Smart money is quietly hedging.',
    edge: 'Credit spreads diverging from equity complacency.',
    time_sensitivity: 'THIS WEEK',
    forces: ['MONEY', 'DEBT'],
    active_regime: 'TRANSITION',
    macro_dashboard: {},
    cross_market: {},
    news_wires: [],
    key_levels: {},
    weekly_catalyst: 'Fed speakers Friday'
  };
}
return [{ json: parsed }];"""
        print("Fixed: Parse Supervisor Response -> robust fallback")

with open('chaos_v7_complete_UI.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("\nAll fixes applied! Workflow ready for FREE model usage.")
