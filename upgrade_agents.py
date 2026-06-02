import re
import os

with open('src/openrouter-agents.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add Fallback arrays at the top
fallback_consts = """const NARRATIVE_FALLBACK_MODELS = [
  "meta-llama/llama-3.3-70b-instruct:free",
  "google/gemini-2.5-flash:free",
  "qwen/qwen-2.5-72b-instruct:free"
];
const PARSER_FALLBACK_MODELS = [
  "google/gemini-2.5-flash:free",
  "meta-llama/llama-3.3-70b-instruct:free",
  "mistralai/mistral-7b-instruct:free"
];
"""
js = js.replace('const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";', 'const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";\n\n' + fallback_consts)

# 2. Update callOpenRouter to handle model arrays
old_call = """export async function callOpenRouter(prompt, model, env = process.env) {
  if (!env.OPENROUTER_API_KEY) throw new Error("OPENROUTER_API_KEY is not configured.");

  const res = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": env.OPENROUTER_SITE_URL ?? "https://chaos.sumanthworks.com",
      "X-Title": env.OPENROUTER_APP_NAME ?? "Chaos Intelligence"
    },
    body: JSON.stringify({
      model,
      messages: [{ role: "user", content: prompt }],
      temperature: 0.55,
      max_tokens: model === DEFAULT_MODELS.supervisor ? 3500 : 900
    })
  });
  if (!res.ok) throw new Error(`OpenRouter error ${res.status}: ${await res.text()}`);
  const json = await res.json();
  return json?.choices?.[0]?.message?.content ?? "";
}"""

new_call = """export async function callOpenRouter(prompt, modelOrModels, env = process.env) {
  if (!env.OPENROUTER_API_KEY) throw new Error("OPENROUTER_API_KEY is not configured.");

  const isArray = Array.isArray(modelOrModels);
  const reqBody = {
    messages: [{ role: "user", content: prompt }],
    temperature: 0.55,
    max_tokens: (!isArray && modelOrModels === DEFAULT_MODELS.supervisor) ? 3500 : 1500
  };
  
  if (isArray) {
    reqBody.models = modelOrModels;
  } else {
    reqBody.model = modelOrModels;
  }

  const res = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": env.OPENROUTER_SITE_URL ?? "https://chaos.sumanthworks.com",
      "X-Title": env.OPENROUTER_APP_NAME ?? "Chaos Intelligence"
    },
    body: JSON.stringify(reqBody)
  });
  if (!res.ok) throw new Error(`OpenRouter error ${res.status}: ${await res.text()}`);
  const json = await res.json();
  if (!json.choices || json.choices.length === 0) {
    throw new Error(`OpenRouter Empty Response Frame: ${JSON.stringify(json)}`);
  }
  return json.choices[0].message.content ?? "";
}"""

js = js.replace(old_call, new_call)

# 3. Replace the buildSupervisorPrompt with the Cinematic Prompt
old_supervisor_prompt = re.search(r'export function buildSupervisorPrompt\(data, agents\) \{.*?^\}', js, re.DOTALL | re.MULTILINE).group(0)

new_supervisor_prompt = """export function buildSupervisorPrompt(data, agents) {
  return `You are the world’s most addictive financial macro writer. Your style combines the brilliant, ironic wit of Matt Levine's 'Money Stuff' with the pure, cinematic suspense of an Arthur Hayes essay. You write for global prediction market whales and crypto native executioners.

CRITICAL ENGAGEMENT LAWS:
1. NEVER speak like a traditional AI bot or academic textbook. Zero safe filler summaries.
2. ABSOLUTELY FORBIDDEN TERMS: If you print the words "delve", "testament", "in conclusion", "crucial", "furthermore", "moreover", "landscape", "pivotal", or "beacon", your engine will fail.
3. KILL THE PARAGRAPH NOISE: Write in short, high-impact rhythmic sentences. Mix razor-short fragments with deep analytical variables to anchor user attention.
4. THE REAL-WORLD METAPHOR: You must compare the current divergence to a high-stress scenario (e.g., high-speed chicken, a crowded room smelling smoke, a coiled monster spring, a predatory hunting line).

AGENTS CONTEXT:
Fundamental: ${agents.fundamental.bias} ${agents.fundamental.confidence}% - ${agents.fundamental.thesis}
Technical: ${agents.technical.bias} ${agents.technical.confidence}% - ${agents.technical.thesis}
Sentiment: ${agents.sentiment.bias} ${agents.sentiment.confidence}% - ${agents.sentiment.thesis}

LIVE DATA:
- Session: ${data.label}
- Fear: ${data.fearIndex} (${data.fearLabel}), delta ${data.fearDelta}
- BTC: ${data.btcPrice} (${data.btcChange}%)
- VIX: ${data.vixVal}
- 10Y: ${data.yieldVal}%
- DXY: ${data.dxyVal}
- SPX: ${data.spxVal} (${data.spxChange})

OUTPUT LAYOUT STRUCTURING:
You must output exactly this schema structure with zero variations:

### THE BLOCKBUSTER HEADLINE
[Write one massive, unforgettable, contrarian headline. Max 12 words. Cut all end punctuation.]

### THE CINEMATIC SUMMARY
[Write exactly 3 distinct sentences.
Sentence 1: Hook the reader using your high-tension real-world metaphor.
Sentence 2: Use HTML <strong> tags to bold the first 4 words. Call out the raw divergence between local crypto fear and healthy equities (VIX/SPX).
Sentence 3: Expose the market trap showing how institutional bots are exploiting retail emotion as exit liquidity.]

### PLAY 1: THE SAFE LINE
**The Narrative:** [1 sentence explaining why lagging algorithms are waiting here.]
**The Exact Trigger:** [State the explicit level clearly.]

### PLAY 2: THE WHALE HUNT (AGGRESSIVE)
**The Narrative:** [1 sentence explaining how to front-run the machine before the turn.]
**The Exact Trigger:** [State the aggressive value number.]

### PLAY 3: THE LIQUIDATION SQUEEZE (CONTRARIAN)
**The Narrative:** [1 sentence tracking where trapped short liquidity handles sit.]
**The Exact Trigger:** [State the macro target breakout value.]`;
}"""

js = js.replace(old_supervisor_prompt, new_supervisor_prompt)

# 4. Update runAgents to use NARRATIVE_FALLBACK_MODELS and parse the Markdown output!
old_runAgents = re.search(r'export async function runAgents\(data, env = process.env\) \{.*?^\}', js, re.DOTALL | re.MULTILINE).group(0)

new_runAgents = """export async function runAgents(data, env = process.env) {
  if (!env.OPENROUTER_API_KEY) return fallbackAgents(data);

  const prompts = buildAgentPrompts(data);
  const [fundRaw, techRaw, sentRaw] = await Promise.all([
    callOpenRouter(prompts.fundamental, PARSER_FALLBACK_MODELS, env),
    callOpenRouter(prompts.technical, PARSER_FALLBACK_MODELS, env),
    callOpenRouter(prompts.sentiment, PARSER_FALLBACK_MODELS, env)
  ]);

  const fundamental = validateAgentOutput(fundRaw, "FUNDAMENTAL");
  const technical = validateAgentOutput(techRaw, "TECHNICAL");
  const sentiment = validateAgentOutput(sentRaw, "SENTIMENT");
  
  const supRaw = await callOpenRouter(
    buildSupervisorPrompt(data, { fundamental, technical, sentiment }),
    NARRATIVE_FALLBACK_MODELS,
    env
  );
  
  // PARSE THE CINEMATIC MARKDOWN OUTPUT
  let headline = "Market Regime Transition In Progress.";
  let eli5 = "Macro volatility indexes remain silent while localized liquidation sweeps leverage.";
  let plays = [
    { type: "SAFE", thesis: "Awaiting confirmation.", details: "Levels unconfirmed." },
    { type: "AGGRESSIVE", thesis: "Awaiting intel.", details: "Execution pending." },
    { type: "CONTRARIAN", thesis: "Awaiting liquidity.", details: "Squeeze undefined." }
  ];

  const hlMatch = supRaw.match(/### THE BLOCKBUSTER HEADLINE\\n([\\s\\S]*?)(?=\\n\\n###|\\n$|$)/);
  if (hlMatch) headline = hlMatch[1].trim();
  
  const cinMatch = supRaw.match(/### THE CINEMATIC SUMMARY\\n([\\s\\S]*?)(?=\\n\\n###|\\n$|$)/);
  if (cinMatch) eli5 = cinMatch[1].trim().replace(/\\n/g, " ");

  const p1Match = supRaw.match(/### PLAY 1: THE SAFE LINE\\n\\*\\*The Narrative:\\*\\* ([\\s\\S]*?)\\n\\*\\*The Exact Trigger:\\*\\* ([\\s\\S]*?)(?=\\n\\n###|\\n$|$)/);
  if (p1Match) plays[0] = { type: "SAFE", thesis: p1Match[1].trim(), details: p1Match[2].trim() };

  const p2Match = supRaw.match(/### PLAY 2: THE WHALE HUNT \\(AGGRESSIVE\\)\\n\\*\\*The Narrative:\\*\\* ([\\s\\S]*?)\\n\\*\\*The Exact Trigger:\\*\\* ([\\s\\S]*?)(?=\\n\\n###|\\n$|$)/);
  if (p2Match) plays[1] = { type: "AGGRESSIVE", thesis: p2Match[1].trim(), details: p2Match[2].trim() };

  const p3Match = supRaw.match(/### PLAY 3: THE LIQUIDATION SQUEEZE \\(CONTRARIAN\\)\\n\\*\\*The Narrative:\\*\\* ([\\s\\S]*?)\\n\\*\\*The Exact Trigger:\\*\\* ([\\s\\S]*?)(?=\\n\\n###|\\n$|$)/);
  if (p3Match) plays[2] = { type: "CONTRARIAN", thesis: p3Match[1].trim(), details: p3Match[2].trim() };

  // Calculate standard signal based on the agents' output
  const agentConsensus = summarizeConsensus(fundamental, technical, sentiment, undefined);
  let signal = agentConsensus.signal || "VOLATILE";
  let confidence = agentConsensus.confidence || 60;
  
  const supervisor = {
    headline,
    chaos_line: headline, // Mapping blockbuster headline to chaos_line for consistency
    eli5,
    signal,
    confidence,
    plays,
    trap: "Market trapped in local narrative divergence.",
    edge: "VIX remains unconfirmed by equities.",
    time_sensitivity: "IMMEDIATE",
    forces: ["MONEY", "TECH"],
    active_regime: "TRANSITION",
    agent_consensus: agentConsensus
  };
  
  return { fundamental, technical, sentiment, supervisor };
}"""

js = js.replace(old_runAgents, new_runAgents)

with open('src/openrouter-agents.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("openrouter-agents.js fully upgraded.")
